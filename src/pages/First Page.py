# Environment Setting
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import modules.oneDataLoading as DataLoading
import modules.oneConfiguration as Configuration
import modules.oneStyling as Styling
import modules.onePlot as Plot

# Style
Styling.TopBar(logoUrl=Configuration.WeRoadLogo)

# Load Data
@st.cache_data
def LoadAndTransformData(inputFilePath, percentages, lags):
    originalDf  = DataLoading.LoadData(inputFilePath)
    unpivotedDf = DataLoading.UnpivotData(originalDf, percentages)
    df  = DataLoading.AddCAC(unpivotedDf)
    df  = DataLoading.AddPromo(originalDf, df)
    df  = DataLoading.AddTicketPreSales(originalDf, df)
    df  = DataLoading.AddTimeIntelligence(df)
    df  = DataLoading.AddLaggedCost(df, lags)    
    df = DataLoading.RoundNumericColumns(df)
    
    return df

df = LoadAndTransformData(Configuration.InputPath, Configuration.Percentages, Configuration.LagsInWeeks)

# Plots
col1, col2 = st.columns(2)
with col1: Channel = Styling.RenderFilter(['All', 'Pull', 'PPC', 'Push', 'Criteo', 'Facebook', 'Instagram', 'TikTok'], label='Channel')
with col2: Lag = Styling.RenderFilter(Configuration.LagsInWeeks, label='Lag (weeks)')

col1, col2, col3 = st.columns(3)
with col1:
    ImpressionPlot = Plot.CreateImpressionsPlot(df, Channel, Lag)
    ImpressionPlot = Styling.RenderChannelVsCostPlot(ImpressionPlot, Channel, Lag, 'Impressions')
    st.plotly_chart(ImpressionPlot, use_container_width=True)
with col2:
    ClicksPlot = Plot.CreateClicksPlot(df, Channel, Lag)
    ClicksPlot = Styling.RenderChannelVsCostPlot(ClicksPlot, Channel, Lag, 'Clicks')
    st.plotly_chart(ClicksPlot, use_container_width=True)
with col3:
    BuyersPlot = Plot.CreateBuyersPlot(df, Channel, Lag)
    BuyersPlot = Styling.RenderChannelVsCostPlot(BuyersPlot, Channel, Lag, 'Buyers')
    st.plotly_chart(BuyersPlot, use_container_width=True)

CACPlot = Plot.CreateCACPlot(df, Channel)
CACPlot = Styling.RenderCACPlot(CACPlot, Channel)
st.plotly_chart(CACPlot, use_container_width=True)

# Table
filteredDf = Plot.FilterTable(df, Channel, Lag)
Styling.RenderTable(filteredDf, 'Filtered Data')