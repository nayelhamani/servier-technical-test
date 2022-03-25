from datetime import datetime

import pandas as pd


def read_csv(filepath):
    return pd.read_csv(filepath, encoding='utf-8')


def lower_df(df):
    return df.applymap(lambda s: s.lower() if type(s) == str else s)


def format_date(df, column):
    df[column] = pd.to_datetime(df[column])
    return df


def join_drugs_and_title(drugs_df, title_df, title_column):
    # https://stackoverflow.com/questions/51955386/pandas-dataframe-merge-based-on-str-contains
    r = '({})'.format('|'.join(drugs_df.drug))
    merge_df = title_df[title_column].str.extract(r, expand=False).fillna(title_df[title_column])
    title_mention = drugs_df.merge(title_df, left_on='drug', right_on=merge_df, how='inner')
    return title_mention
