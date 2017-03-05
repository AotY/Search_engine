# coding: UTF-8

import pandas as pd


def get_fre():
    df = pd.read_csv('../data/apriori.csv')
    df.columns = ['name', 'value']
    gdf = df.groupby('name').sum()
    gdf.sort_values(by='value', ascending=False)
    gdf.to_csv('../data/analysis/user_freq.csv')


if __name__ == "__main__":
    get_fre()
