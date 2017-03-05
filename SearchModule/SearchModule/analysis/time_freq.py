# coding: UTF-8

import pandas as pd
import numpy as np


def get_time_freq():
    df = pd.read_csv('../data/query.csv')
    df.columns = ['time', 'query']

    df['time'] = pd.to_datetime(df['time'])
    df['count'] = np.ones(len(df))

    # a list of "1" to count the hashtags
    ones = [1] * len(df['time'])
    # the index of the series
    idx = pd.DatetimeIndex(df['time'])
    # the actual series (at series of 1s for the moment)
    time_fre = pd.Series(ones, index=idx)

    # Resampling / bucketing 3T
    per_minute = time_fre.resample('1H', how='sum').fillna(0)

    print(df)
    # gdf = df.groupby(by='class').sum()

    # gdf.sort_values(by='value', ascending=False)
    per_minute.to_csv('../data/analysis/time_fre.csv')


if __name__ == "__main__":
    get_time_freq()
