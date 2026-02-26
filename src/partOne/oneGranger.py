# Environment Setting
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

# Functions | Granger Test
def GrangerTestByGroup(df, groupColumn, groupList, maxLags):
    results = {}  
    
    for group in groupList:
        dfFiltered         = df[df[groupColumn] == group].dropna(subset=['Buyers', 'Cost']).copy()
        observationsNumber = len(dfFiltered)
            
        if observationsNumber < maxLags * 1.5: continue  
        
        result = grangercausalitytests(dfFiltered[['Buyers', 'Cost']], maxlag=maxLags)
        results[group] = result 
    
    return results

def ExtractPValues(results):
    rows = []
    for group, result in results.items():
        for lag, lagData in result.items():
            tests = lagData[0]
            rows.append({'Group': group, 'Lag': lag, 'pValue': tests['ssr_ftest'][1],})
    return pd.DataFrame(rows)