import json
from jsoncomment import JsonComment

import pandas as pd


def read_csv(filepath):
    return pd.read_csv(filepath)

def read_json_to_df(filepath):
    with open(filepath) as data_file:
        parser = JsonComment(json) #handle trailing comma in json
        data = parser.load(data_file)
    return pd.DataFrame(data)

def delete_chars(df):
    df = df.applymap(lambda s: s.replace("\\xc3\\xb1", "") if type(s) == str else s)
    return df.applymap(lambda s: s.replace("\\xc3\\x28", "") if type(s) == str else s)

def lower_df(df):
    return df.applymap(lambda s: s.lower() if type(s) == str else s)


def format_date(df, column):
    df[column] = pd.to_datetime(df[column])
    return df


def join_drugs_and_title(drugs_df, title_df):
    # https://stackoverflow.com/questions/51955386/pandas-dataframe-merge-based-on-str-contains
    r = '({})'.format('|'.join(drugs_df.drug))
    merge_df = title_df.title.str.extract(r, expand=False).fillna(title_df.title)
    title_mention = drugs_df.merge(title_df, left_on='drug', right_on=merge_df, how='inner')
    return title_mention
