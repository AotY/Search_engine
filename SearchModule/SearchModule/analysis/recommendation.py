# coding: UTF-8

import pandas as pd
import numpy as np


def get_recomm():
    df = pd.read_csv('../data/class_.csv')
    df.columns = ['time', 'query', 'class']
    df['count'] = np.ones(len(df))
    gdf = df.groupby(by='class').sum()

    # gdf.sort_values(by='value', ascending=False)
    gdf.to_csv('../data/analysis/user_recomm.csv')


if __name__ == "__main__":
    get_recomm()
