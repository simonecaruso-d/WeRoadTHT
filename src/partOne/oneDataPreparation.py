# Environment Setting
import numpy as np
import pandas as pd

# Functions | Data Loading
def LoadData(inputFilePath):    
    df = pd.read_excel(inputFilePath, sheet_name='weekly overview')

    return df

def UnpivotData(df, percentages):
    rows = []
    
    for idx, row in df.iterrows():
        date     = row['Monday']       
        channels = {
            'Facebook'   : {'Cost'       : row['Facebook €'], 
                            'Click'      : row['Facebook l-click'], 
                            'Impressions': row['Facebook Imp.'], 
                            'Buyers'     : row['1st Time Buyer'] * percentages['facebook']},
            'Instagram'  : {'Cost'       : row['Instagram €'], 
                            'Click'      : row['Instagram l-click'], 
                            'Impressions': row['Instagram Imp.'], 
                            'Buyers'     : row['1st Time Buyer'] * percentages['instagram']},
            'TikTok'     : {'Cost'       : row['TikTok €'], 
                            'Click'      : row['TikTok click'], 
                            'Impressions': row['TikTok imp.'], 
                            'Buyers'     : row['1st Time Buyer'] * percentages['tiktok']},
            'Criteo'     : {'Cost'       : row['Criteo €'], 
                            'Click'      : row['Criteo click'], 
                            'Impressions': row['Criteo imp.'], 
                            'Buyers'     : row['1st Time Buyer'] * percentages['criteo']},
            'Push'       : {'Cost'       : row['Facebook €'] + row['Instagram €'] + row['TikTok €'] + row['Criteo €'], 
                            'Click'      : row['Facebook l-click'] + row['Instagram l-click'] + row['TikTok click'] + row['Criteo click'], 
                            'Impressions': row['Facebook Imp.'] + row['Instagram Imp.'] + row['TikTok imp.'] + row['Criteo imp.'], 
                            'Buyers'     : row['1st Time Buyer'] * (percentages['facebook'] + percentages['instagram'] + percentages['tiktok'] + percentages['criteo'])},
            
            'PPC'        : {'Cost'       : row['PPC Brand €'] + row['PPC Generic €'], 
                            'Click'      : row['PPC Brand click'] + row['PPC Generic click'], 
                            'Impressions': None, 
                            'Buyers'      : row['1st Time Buyer'] * percentages['ppc']},
            'Google'     : {'Cost'       : None, 
                            'Click'      : row['SEO Clicks'], 
                            'Impressions': None,
                            'Buyers'      : row['1st Time Buyer'] * percentages['google']},
            'WordOfMouth': {'Cost'       : None,
                            'Click'      : None, 
                            'Impressions': None, 
                            'Buyers'      : row['1st Time Buyer'] * percentages['wordofmouth']},
            'Other'      : {'Cost'       : None,
                            'Click'      : None, 
                            'Impressions': None, 
                            'Buyers'      : row['1st Time Buyer'] * percentages['other']},
            'Pull'       : {'Cost'       : row['PPC Brand €'] + row['PPC Generic €'],
                            'Click'      : row['PPC Brand click'] + row['PPC Generic click'] + row['SEO Clicks'],
                            'Impressions': None,
                            'Buyers'      : row['1st Time Buyer'] * (percentages['ppc'] + percentages['google'] + percentages['wordofmouth'] + percentages['other'])},
                            
            'All'        : {'Cost'       : row['Facebook €'] + row['Instagram €'] + row['TikTok €'] + row['Criteo €'] + row['PPC Brand €'] + row['PPC Generic €'],
                            'Click'      : row['Facebook l-click'] + row['Instagram l-click'] + row['TikTok click'] + row['Criteo click'] + row['PPC Brand click'] + row['PPC Generic click'] + row['SEO Clicks'],
                            'Impressions': row['Facebook Imp.'] + row['Instagram Imp.'] + row['TikTok imp.'] + row['Criteo imp.'],
                            'Buyers'      : row['1st Time Buyer']}}
        
        for channelName, metrics in channels.items():rows.append({'Date': date, 'Channel': channelName, 'Cost': metrics['Cost'], 'Click': metrics['Click'], 'Impressions': metrics['Impressions'], 'Buyers': metrics['Buyers']})
    
    return pd.DataFrame(rows)

# Functions | Data Cleaning
def DropDuplicates(df):
    df = df.drop_duplicates()
    return df

def RoundNumericColumns(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]): df[col] = df[col].round(2)
    return df

# Functions | Data Engineering
def AddTimeIntelligence(df):
    df['Season']    = df['Date'].dt.month.apply(lambda x: 'Winter' if x in [12, 1, 2] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Autumn')))
    df['Month']     = df['Date'].dt.month
    df['Week']      = df['Date'].dt.isocalendar().week
    df['MonthSin']  = np.sin(2 * np.pi * df['Month'] / 12)
    df['MonthCos']  = np.cos(2 * np.pi * df['Month'] / 12)
    df['WeekSin']   = np.sin(2 * np.pi * df['Week'] / 52)
    df['WeekCos']   = np.cos(2 * np.pi * df['Week'] / 52)
    df['DayOfWeek'] = df['Date'].dt.dayofweek

    return df.drop(['Month', 'Week'], axis=1)