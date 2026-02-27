import pandas as pd
import tabulate

import twoADataPreparation as DataLoading
import twoAModel as Model
import twoAConfiguration as Configuration

# Pipelines
def PaidPipeline(df, channels, decay, window, testDays, growthType, seasonalityMode, seasonalities):
    df                   = DataLoading.ApplyRollingAdstockLog(df, channels, decay=decay, window=window)
    df                   = DataLoading.PreparePaidDataframe(df, channels) 
    train, test          = Model.TrainTestSplit(df, testDays)
    model                = Model.FitModel(channels, train, 'Paid', growthType, seasonalityMode, seasonalities)
    trainMape, trainRmse = Model.TestModel(model, train)
    testMape, testRmse   = Model.TestModel(model, test)
    return trainMape, trainRmse, testMape, testRmse

def OrganicPipeline(df, lags, testDays, growthType, seasonalityMode, seasonalities):
    df                   = DataLoading.PrepareOrganicDataframe(df, lags) 
    train, test          = Model.TrainTestSplit(df, testDays)
    model                = Model.FitModel([], train, 'Organic', growthType, seasonalityMode, seasonalities)
    trainMape, trainRmse = Model.TestModel(model, train)
    testMape, testRmse   = Model.TestModel(model, test)
    return trainMape, trainRmse, testMape, testRmse

# Run
df = DataLoading.DataLoading(Configuration.ExcelFilePath)

Channels = [col for col in df.columns if col.endswith('€')]
Lags     = Configuration.Lags
Decay    = Configuration.Decay
Window   = Configuration.Window

TestDays        = Configuration.TestDays
Seasonalities   = Configuration.Seasonalities
GrowthType      = Configuration.GrowthType
SeasonalityMode = Configuration.SeasonalityMode

PaidTrainMape, PaidTrainRmse, PaidTestMape, PaidTestRmse             = PaidPipeline(df, Channels, Decay, Window, TestDays, GrowthType, SeasonalityMode, Seasonalities)
OrganicTrainMape, OrganicTrainRmse, OrganicTestMape, OrganicTestRmse = OrganicPipeline(df, Lags, TestDays, GrowthType, SeasonalityMode, Seasonalities)

Results     = pd.DataFrame([['Paid Sessions', f'{PaidTrainRmse:.2f}', f'{PaidTestRmse:.2f}', f'{PaidTrainMape:.2%}', f'{PaidTestMape:.2%}'], 
                            ['Organic Sessions', f'{OrganicTrainRmse:.2f}', f'{OrganicTestRmse:.2f}', f'{OrganicTrainMape:.2%}', f'{OrganicTestMape:.2%}']], 
                            columns=['Model', 'Train RMSE', 'Test RMSE', 'Train MAPE', 'Test MAPE'])
print(tabulate.tabulate(Results, headers='keys', tablefmt='psql', showindex=False))