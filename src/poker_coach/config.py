# These are the file paths used 
DATA_DIR = "../Data"
BUSTABIT_DATA_FILE = f"{DATA_DIR}/bustabit.csv"

#Bustabit data scheme and columns
DATA_COLUMNS = ['Bet','CashedOut', 'Bonus', 'Profit', 'BustedAt']
ID_COLS = ['Id', 'GameID']

# Shared Visualization Palettes
GRAPE_SODA = "#8a4f7d"
MUTED_TEAL = "#88a096"
ROSY_GRANITE = "#887880"
KHAKI_BEIGE = "#BBAB8B"
SWEET_SALMON = "#ef8275"

KPI_TEXT_PROPS = [
    {"color": "blue", "fontweight": "bold"},  # ex. in loss_chasing_analysis color applied to (Statistic) in the chart
    {"color": "red", "fontweight": "bold"}   # in loss_chasing_analysis color applied to (P-Value) in chart
]