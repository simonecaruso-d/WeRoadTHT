import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error

# Train Test Split
def TrainTestSplit(df, testDays):
    splitDate = df['ds'].max() - pd.Timedelta(days=testDays)
    train     = df[df['ds'] <= splitDate]
    test      = df[df['ds'] > splitDate]
    
    return train, test

# Prophet
def FitModel(channels, train, modelType, growthType, seasonalityMode, seasonalities):    
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False, growth=growthType, seasonality_mode=seasonalityMode)
    for name, period, fourierOrder in seasonalities: model.add_seasonality(name=name, period=period, fourier_order=fourierOrder)
    
    if modelType == 'Paid':
        for col in channels: model.add_regressor(col + 'Adstock', standardize='auto')
    else:
        for col in train.columns:
            if col not in ['ds', 'y', 'cap']: model.add_regressor(col, standardize='auto')
        
    model.fit(train)
    
    return model

def TestModel(model, test):
    forecast    = model.predict(test)

    predictions = np.expm1(forecast['yhat'].values)
    actuals     = np.expm1(test['y'].values)
    
    mape = mean_absolute_percentage_error(actuals, predictions)
    rmse = np.sqrt(np.mean((predictions - actuals) ** 2))

    return mape, rmse