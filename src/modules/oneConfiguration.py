# Environment Setting
from pathlib import Path

# Paths
ProjectRoot = Path(__file__).parent.parent.parent
InputPath   = ProjectRoot / 'data' / 'BCWeeklyDataMarketing.xlsx'

# Personal Inputs
Percentages = {'facebook': 0.14, 'instagram': 0.21, 'tiktok': 0.04, 'criteo': 0.02, 'ppc': 0.03, 'google': 0.12, 'wordofmouth': 0.4, 'other': 0.04}
LagsInWeeks =[1, 2, 4, 8, 12, 16]

# URLs
WeRoadLogo = 'https://learnn.com/wp-content/uploads/2024/06/weroad_color-01.jpg'

# Colors
ColorPrimary    = '#ff4759'
ColorSecondary  = '#668EEA'
ColorCACPrimary = '#27ae60'
ColorCACSecondary = '#f39c12'
ColorWhite      = '#ffffff'
ColorDark       = '#0f0f0f'
ColorBackground = '#ffffff'
ColorText       = '#333333'
ColorTopBar     = '#f8f8f8'
ColorGrayLight  = '#d0d0d0'
ColorGrayDarker = '#555555'