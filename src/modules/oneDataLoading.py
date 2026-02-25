# Environment Setting
import pandas as pd

# Load
def LoadData(inputFilePath):    
    df = pd.read_excel(inputFilePath, sheet_name='weekly overview')

    return df

# Unpivot
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
        
        for channelName, metrics in channels.items():rows.append({'Date'       : date,
                                                                  'Channel'    : channelName,
                                                                  'Cost'       : metrics['Cost'],
                                                                  'Click'      : metrics['Click'],
                                                                  'Impressions': metrics['Impressions'],
                                                                  'Buyers'     : metrics['Buyers']})
    
    return pd.DataFrame(rows)

# Enrich
def AddCAC(df):
    df = df.sort_values(['Channel', 'Date']).reset_index(drop=True)
    
    df['RunningCost']   = df.groupby('Channel')['Cost'].transform(lambda x: x.fillna(0).cumsum())
    df['RunningBuyers'] = df.groupby('Channel')['Buyers'].transform(lambda x: x.cumsum())
    df['CAC']           = df.apply(lambda row: row['RunningCost'] / row['RunningBuyers'], axis=1)
    
    return df.drop(['RunningCost', 'RunningBuyers'], axis=1)

def AddPromo(originalDf, unpivotedDf):
    unpivotedDf          = unpivotedDf.merge(originalDf[['Monday', 'note']], left_on='Date', right_on='Monday', how='left').drop('Monday', axis=1)
    
    unpivotedDf['Promo'] = unpivotedDf['note'].fillna('').str.strip()
    unpivotedDf['Promo'] = unpivotedDf['Promo'].replace('', None) 
    
    return unpivotedDf.drop('note', axis=1)

def AddTicketPreSales(originalDf, unpivotedDf):
    unpivotedDf                   = unpivotedDf.merge(originalDf[['Monday', 'Ticket Pre-sales']], left_on='Date', right_on='Monday', how='left').drop('Monday', axis=1)
    
    meanTickets                   = originalDf['Ticket Pre-sales'].mean()
    stdTickets                    = originalDf['Ticket Pre-sales'].std()
    threshold                     = meanTickets + stdTickets
    unpivotedDf['TicketPeakFlag'] = (unpivotedDf['Ticket Pre-sales'] > threshold).astype(int)
    
    return unpivotedDf.drop('Ticket Pre-sales', axis=1)

def AddTimeIntelligence(df):
    df['Year']      = df['Date'].dt.year
    df['Season']    = df['Date'].dt.month.apply(lambda x: 'Winter' if x in [12, 1, 2] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Autumn')))
    df['Quarter']   = df['Date'].dt.quarter
    df['Month']     = df['Date'].dt.month
    df['Week']      = df['Date'].dt.isocalendar().week
    df['DayOfWeek'] = df['Date'].dt.day_name()

    return df

def RoundNumericColumns(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]): df[col] = df[col].round(2)
    return df

# Lagged Features
def AddLaggedCost(df, lags):
    df = df.sort_values(['Channel', 'Date']).reset_index(drop=True)
    
    for lag in lags: df[f'CostLag{lag}'] = df.groupby('Channel')['Cost'].shift(lag)
    return df