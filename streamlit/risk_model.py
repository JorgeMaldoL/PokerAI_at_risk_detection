"""Wraps models/xgboost_risk_screener.pkl (trained in
notebooks/05_training_and_testing.ipynb on the bustabit dataset) so a live
poker session's betting pattern can be screened the same way.

Caveat: the model was trained on bustabit "bits" units, not poker big blinds.
Feeding BB-denominated session stats directly is a reasonable approximation
for a proof of concept, not a calibrated screening tool.
"""
import joblib

from poker_coach.config import RISK_SCREENER_MODEL_FILE

FEATURE_COLUMNS = ["average_bet", "max_bet", "win_rate", "total_profit"]

# The saved model is a bare XGBClassifier with no label encoder alongside it.
# sklearn's LabelEncoder sorts string classes alphabetically, and the only
# three tier strings notebooks/05 ever produces are 'Low' / 'Moderate' /
# 'High', so this order is deterministic.
TIER_LABELS = ["High", "Low", "Moderate"]

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(RISK_SCREENER_MODEL_FILE)
    return _model


def predict_risk_tier(average_bet: float, max_bet: float, win_rate: float, total_profit: float) -> dict:
    model = _get_model()
    features = [[average_bet, max_bet, win_rate, total_profit]]
    proba = model.predict_proba(features)[0]
    tier_idx = int(proba.argmax())
    return {
        "tier": TIER_LABELS[tier_idx],
        "probabilities": {label: round(float(p), 3) for label, p in zip(TIER_LABELS, proba)},
    }
