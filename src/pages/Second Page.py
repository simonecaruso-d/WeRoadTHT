import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import modules.configuration as Configuration
import modules.styling as Styling

# Style
Styling.TopBar(logoUrl=Configuration.WeRoadLogo)

st.title('📊 Page Two')
st.markdown('Coming soon...')
