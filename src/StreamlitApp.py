import streamlit as st

# Configure page
st.set_page_config(page_title='WeRoad THT', page_icon='🔬', layout='wide')

# Title and intro
st.title('🔬 WeRoad Take Home Test')
st.markdown('---')

st.markdown("""
### Welcome to the WeRoad Dashboard for the Take Home Test by Simone Caruso!

This application provides comprehensive graphs on manipulated data that allow to answer the questions in the assignment!
The pages are strictly linked to each question, so feel free to explore them in any order you like.
You can find the dataset, the assignment, and the code used to manipulate it in the GitHub repository where you found this link.

**Author:** Simone Caruso  
**Date:** February 2026
""")

st.info('Select a page from the sidebar to start exploring the data!')
