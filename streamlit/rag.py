"""Retrieval-augmented grounding for the Learning Coach.

Fits a small TF-IDF index over the GTO scenario data already in this repo
(the `scenarios` table in poker_coach's SQLite DB, seeded from
Data/sample_scenarios.json) and uses the nearest spots to ground the coach's
suggested frequencies, then runs them through poker_coach.api.coach.get_coaching
for a natural-language verdict (LLM-backed, with a built-in fallback when no
Gemini/Vertex credentials are configured).
"""
import threading
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from poker_coach.api import database
from poker_coach.api.coach import _fallback_coaching, get_coaching
from poker_coach.config import DATA_DIR
from poker_coach.ingest import ingest, load_scenarios

_COACHING_TIMEOUT_S = 3.0

_corpus: list[dict] = []
_vectorizer: TfidfVectorizer | None = None
_matrix = None


def _describe(scenario: dict) -> str:
    street = {0: "preflop", 3: "flop", 4: "turn", 5: "river"}.get(
        len(scenario["board"].split()), "postflop"
    )
    gto = scenario["gto_strategy"]
    dominant = max(gto, key=gto.get)
    return (
        f"{street} spot in position {scenario['position']} "
        f"after {scenario.get('opponent_action') or 'no action'}, "
        f"favored action {dominant}"
    )


def _seed_corpus_from_repo_data() -> None:
    """Make sure the scenario DB also has the repo's sample scenarios, not
    just the 4 rows poker_coach.api.database.init_db() auto-seeds."""
    database.init_db()
    conn = database.get_connection()
    try:
        seen = {(s["board"], s["hole_cards"]) for s in database.list_scenarios(conn)}
    finally:
        conn.close()
    sample_path = DATA_DIR / "sample_scenarios.json"
    if not sample_path.exists():
        return
    new_scenarios = [
        s for s in load_scenarios(sample_path) if (s["board"], s["hole_cards"]) not in seen
    ]
    if new_scenarios:
        ingest(new_scenarios)


def _ensure_index() -> None:
    global _corpus, _vectorizer, _matrix
    if _vectorizer is not None:
        return
    _seed_corpus_from_repo_data()
    conn = database.get_connection()
    try:
        _corpus = database.list_scenarios(conn)
    finally:
        conn.close()
    texts = [_describe(s) for s in _corpus] or ["empty corpus"]
    _vectorizer = TfidfVectorizer()
    _matrix = _vectorizer.fit_transform(texts)


def retrieve_similar(street: str, opponent_action: str, hand_strength: float, k: int = 2) -> list[dict]:
    """Nearest scenarios in the corpus to the live spot, by cosine similarity
    over a short text description. The game is always heads-up so there's no
    real position label to match on — street, opponent action, and the
    action the current hand strength favors carry the retrieval signal."""
    _ensure_index()
    if not _corpus:
        return []
    dominant = "raise" if hand_strength >= 0.6 else "call" if hand_strength >= 0.35 else "fold"
    query = f"{street.lower()} spot after {opponent_action}, favored action {dominant}"
    query_vec = _vectorizer.transform([query])
    sims = cosine_similarity(query_vec, _matrix)[0]
    ranked = sorted(range(len(_corpus)), key=lambda i: sims[i], reverse=True)[:k]
    return [_corpus[i] for i in ranked]


def _blend_mix(mix: dict, reference: dict) -> dict:
    key_map = {"Fold": "fold", "Check/Call": "call", "Bet/Raise": "raise"}
    fallback_map = {"Check/Call": "check", "Bet/Raise": "bet"}
    blended = {}
    for label, value in mix.items():
        ref_val = reference.get(key_map[label], reference.get(fallback_map.get(label, ""), None))
        blended[label] = round((value + ref_val) / 2, 1) if ref_val is not None else value
    return blended


@lru_cache(maxsize=256)
def _cached_coaching(board: str, hole_cards: str, opponent_action: str,
                      pot_size: float, stack_size: float, user_action: str,
                      gto_strategy_items: tuple) -> dict:
    return get_coaching(
        board=board,
        hole_cards=hole_cards,
        position="Heads-up",
        opponent_action=opponent_action,
        pot_size=pot_size,
        stack_size=stack_size,
        user_action=user_action,
        gto_strategy=dict(gto_strategy_items),
    )


def _bounded_coaching(**kwargs) -> dict | None:
    """get_coaching() can take 10+ seconds when it tries (and fails) to reach
    Vertex AI before falling back. Bound that so one hand can't freeze the UI;
    the caller supplies a local fallback if this returns None. Runs on a
    daemon thread so an abandoned slow call can't hang the app on shutdown."""
    result: dict = {}

    def _run():
        try:
            result["value"] = _cached_coaching(**kwargs)
        except Exception:
            pass

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=_COACHING_TIMEOUT_S)
    return result.get("value")


def enrich(feedback: dict, board: str, hole_cards: str, opponent_action: str,
           pot: float, stack: float, raw_action: str) -> dict:
    """Ground a local heuristic feedback dict (see streamlit/app.py's
    coach_feedback) with retrieved similar scenarios and a coaching verdict."""
    similar = retrieve_similar(
        street=feedback["street"],
        opponent_action=opponent_action,
        hand_strength=feedback["estimated_strength"],
    )
    mix = _blend_mix(feedback["mix"], similar[0]["gto_strategy"]) if similar else feedback["mix"]
    gto_strategy = {"fold": mix["Fold"], "call": mix["Check/Call"], "bet": mix["Bet/Raise"]}

    coaching = _bounded_coaching(
        board=board,
        hole_cards=hole_cards,
        opponent_action=opponent_action,
        pot_size=pot,
        stack_size=stack,
        user_action=raw_action,
        gto_strategy_items=tuple(sorted(gto_strategy.items())),
    )
    if coaching is None:
        # Same fallback get_coaching() itself uses when Gemini is unreachable,
        # just reused directly since our timeout fired before it could.
        coaching = _fallback_coaching(raw_action, gto_strategy)
    return {**feedback, "mix": mix, "similar": similar, "coaching": coaching}
