# Environment Setting
from pathlib import Path

# Paths
ProjectRoot = Path(__file__).parent.parent.parent
InputPath   = ProjectRoot / 'data' / 'BCWeeklyDataMarketing.xlsx'

# Personal Inputs
Percentages = {'facebook': 0.25, 'instagram': 0.18, 'tiktok': 0.12, 'criteo': 0.08, 'ppc': 0.22, 'google': 0.10, 'wordofmouth': 0.03, 'other': 0.02}
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