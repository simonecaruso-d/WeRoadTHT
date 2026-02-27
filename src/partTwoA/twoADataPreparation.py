# Environment Setting
import pandas as pd
import numpy as np

# Data Loading
def DataLoading(excelFilePath):
    df       = pd.read_excel(excelFilePath)
    df['ds'] = pd.to_datetime(df['Date'])
    df       = df.sort_values('ds').reset_index(drop=True)
    return df

# Adstock & Log Transformation
def Adstock(series, decay):
    result    = []
    carryover = 0
    
    for value in series:
        carryover = value + decay * carryover
        result.append(carryover)
    
    return np.array(result)

def ApplyRollingAdstockLog(df, channels, decay, window):
    for col in channels:
        smoothed  = df[col].rolling(window=window, min_periods=1).mean()
        adstocked = Adstock(smoothed, decay=decay)
        df[col + 'Adstock'] = np.log1p(adstocked)
    return df

# Prepare Dataframes
def PreparePaidDataframe(df, channels):
    dfPaid      = df[['ds', 'Paid Sessions']].copy()
    dfPaid['y'] = np.log1p(dfPaid['Paid Sessions'])
    
    for col in channels: dfPaid[col + 'Adstock'] = np.log1p(df[col + 'Adstock'])
    
    dfPaid      = dfPaid.drop('Paid Sessions', axis=1)
    dfPaid      = dfPaid.dropna().reset_index(drop=True)

    return dfPaid

def PrepareOrganicDataframe(df, lags):
    dfOrganic      = df[['ds', 'Organic sessions', 'Meta €', 'TikTok €']].copy()
    dfOrganic['y'] = np.log1p(dfOrganic['Organic sessions'])
    
    for lag in lags:
        dfOrganic[f'MetaLag{lag}']   = np.log1p(dfOrganic['Meta €'].shift(lag))
        dfOrganic[f'TikTokLag{lag}'] = np.log1p(dfOrganic['TikTok €'].shift(lag))

    dfOrganic = dfOrganic.drop(['Organic sessions', 'Meta €', 'TikTok €'], axis= 1)
    dfOrganic = dfOrganic.drop(['MetaLag1', 'MetaLag3', 'MetaLag5', 'MetaLag7'], axis=1)
    dfOrganic = dfOrganic.dropna().reset_index(drop=True)

    return dfOrganic