import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('任务3 季节性.xlsx')


columns_to_analyze = ['M101', 'M102', '总和', 'M101合格率', 'M102合格率', '平均']


def test_stationarity(timeseries):
    # 进行ADF测试
    result = adfuller(timeseries)
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    for key, value in result[4].items():
        print('Critical Values:')
        print(f'   {key}, {value}')


def plot_differences(timeseries, column_name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
    timeseries.plot(ax=ax1, title=f'Original Series - {column_name}')
    timeseries.diff().dropna().plot(ax=ax2, title=f'Differenced Series - {column_name}')
    plt.show()


def arima_forecast(series, column_name):
    plot_differences(series, column_name)

    print(f'Stationarity Test for {column_name}')
    test_stationarity(series)

    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()
    print(model_fit.summary())

    # 预测
    forecast = model_fit.forecast(steps=10)
    print(f'Forecast for the next 10 periods of {column_name}:')
    print(forecast)

    # 绘制预测结果
    plt.figure(figsize=(12, 6))
    plt.plot(series, label='Observed')
    plt.plot(forecast, label='Forecast', color='red')
    plt.title(f'Forecast vs Observed for {column_name}')
    plt.legend()
    plt.show()


for col in columns_to_analyze:
    arima_forecast(df[col], col)