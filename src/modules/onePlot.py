# Environment Setting
import pandas as pd
import plotly.graph_objects as go

# Table
def FilterTable(df, channel=None, lag=None):
    filteredDf = df.copy()
    
    if channel and channel != 'All': filteredDf = filteredDf[filteredDf['Channel'] == channel]
    
    if lag is not None:
        lagColumns     = [col for col in filteredDf.columns if col.startswith('CostLag')]
        columnsToDrop  = [col for col in lagColumns if col != f'CostLag{lag}'] + ['Year', 'Season', 'Quarter', 'Month', 'Week', 'DayOfWeek']
        filteredDf     = filteredDf.drop(columns=columnsToDrop, errors='ignore')

    filteredDf['Date'] = pd.to_datetime(filteredDf['Date']).dt.date
    filteredDf         = filteredDf.dropna()
    
    return filteredDf

# Plots
def CreateImpressionsPlot(df, channel, lag=None):
    filteredDf = df[df['Channel'] == channel].copy()
    filteredDf = filteredDf.sort_values('Date').reset_index(drop=True)
    
    if lag is not None: yColumn = f'CostLag{lag}' 
    else: yColumn = 'Cost'
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf[yColumn], name='Cost (€)', mode='lines+markers', yaxis='y'))
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf['Impressions'], name='Impressions', mode='lines+markers', yaxis='y2'))
    
    return fig

def CreateClicksPlot(df, channel, lag=None):
    filteredDf = df[df['Channel'] == channel].copy()
    filteredDf = filteredDf.sort_values('Date').reset_index(drop=True)
    
    if lag is not None: yColumn = f'CostLag{lag}' 
    else: yColumn = 'Cost'
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf[yColumn], name='Cost (€)', mode='lines+markers', yaxis='y'))
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf['Click'], name='Clicks', mode='lines+markers', yaxis='y2'))
    
    return fig

def CreateBuyersPlot(df, channel, lag=None):
    filteredDf = df[df['Channel'] == channel].copy()
    filteredDf = filteredDf.sort_values('Date').reset_index(drop=True)
    
    if lag is not None: yColumn = f'CostLag{lag}' 
    else: yColumn = 'Cost'
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf[yColumn], name='Cost (€)', mode='lines+markers', yaxis='y'))
    fig.add_trace(go.Scatter(x=filteredDf['Date'], y=filteredDf['Buyers'], name='Buyers', mode='lines+markers', yaxis='y2'))
    
    return fig

def CreateCACPlot(df, channel):
    filteredDf = df[df['Channel'] == channel].copy()
    filteredDf = filteredDf.sort_values('Date').reset_index(drop=True)
    
    fig        = go.Figure()
    fig.add_trace(go.Bar(x=filteredDf['Date'], y=filteredDf['CAC'], name='CAC (€)'))

    return fig