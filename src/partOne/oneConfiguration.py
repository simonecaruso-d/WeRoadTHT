# Environment Setting
from pathlib import Path

# Paths
ProjectRoot = Path(__file__).parent.parent.parent
InputPath   = ProjectRoot / 'data' / 'BCWeeklyDataMarketing.xlsx'
ResultsPath = Path(__file__).parent

# Personal Inputs
Percentages = {'facebook': 0.14, 'instagram': 0.21, 'tiktok': 0.04, 'criteo': 0.02, 'ppc': 0.03, 'google': 0.12, 'wordofmouth': 0.4, 'other': 0.04}

# Granger Utilities
ChannelsList = ['All', 'Push', 'Pull']
SeasonsList  = ['Winter', 'Spring', 'Summer', 'Autumn']
MaxLags      = 16