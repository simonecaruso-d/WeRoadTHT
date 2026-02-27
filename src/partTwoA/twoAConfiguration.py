# Environment Setting
from pathlib import Path

# Paths
ExcelFilePath = Path(__file__).parent.parent.parent / 'data' / 'HistoricalDataDailySessions.xlsx'

# Data Preparation
Lags   = [1, 3, 5, 7, 14]
Decay  = 0.9
Window = 5

# Modelling
TestDays        = 45
Seasonalities   = [('weekly', 7, 3), ('monthly', 30.5, 5)]
GrowthType      = 'linear'
SeasonalityMode = 'multiplicative'