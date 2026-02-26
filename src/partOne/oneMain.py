# Environment Setting
import oneConfiguration as Configuration
import oneDataPreparation as DataPreparation
import oneGranger as Granger

# Functions | Helpers
def ETLFunction(excelFilePath, percentages):
    originalDf  = DataPreparation.LoadData(excelFilePath)
    df          = DataPreparation.UnpivotData(originalDf, percentages)
    
    df          = DataPreparation.AddTimeIntelligence(df)

    df          = DataPreparation.DropDuplicates(df)
    df          = DataPreparation.RoundNumericColumns(df)

    return df

def GrangerCycle(df, groupName, groupList, maxLags, outputPath):
    results          = Granger.GrangerTestByGroup(df, groupName, groupList, maxLags)
    extractedResults = Granger.ExtractPValues(results)
    extractedResults.to_excel(outputPath / f'PvaluesGranger{groupName}.xlsx')
    
    return

# Run
df = ETLFunction(Configuration.InputPath, Configuration.Percentages)

GrangerCycle(df, 'Channel', Configuration.ChannelsList, Configuration.MaxLags, Configuration.ResultsPath)
GrangerCycle(df, 'Season', Configuration.SeasonsList, Configuration.MaxLags, Configuration.ResultsPath)