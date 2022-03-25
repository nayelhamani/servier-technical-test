import json

import numpy as np

from utils.utils import read_csv, lower_df, format_date, join_drugs_and_title, delete_chars, read_json_to_df
import pandas as pd


def main():
    start_pipeline()


def start_pipeline():
    drugs_df, pubmed_df, clinical_trials_df = get_files()
    drugs_df, pubmed_df, clinical_trials_df = process_df(drugs_df, pubmed_df, clinical_trials_df)
    nested_df = aggregate_df(drugs_df, pubmed_df, clinical_trials_df)
    result_dict = generate_dict(nested_df)
    write_to_json(result_dict)


def get_files():
    clinical_trials_df = read_csv("ressources/clinical_trials.csv")
    drugs_df = read_csv("ressources/drugs.csv")
    pubmed_df1 = read_csv("ressources/pubmed.csv")
    pubmed_df2 = read_json_to_df("ressources/pubmed.json")
    pubmed_df = pd.concat([pubmed_df1,pubmed_df2]).reset_index(drop=True)
    return drugs_df, pubmed_df, clinical_trials_df


def process_df(drugs_df, pubmed_df, clinical_trials_df):
    # lower str column
    drugs_df = lower_df(drugs_df)
    pubmed_df = lower_df(pubmed_df)
    clinical_trials_df = lower_df(clinical_trials_df)

    # clean characters
    clinical_trials_df = delete_chars(clinical_trials_df)

    # format date
    pubmed_df = format_date(pubmed_df, "date")
    clinical_trials_df = format_date(clinical_trials_df, "date")

    # create and rename columns
    pubmed_df["article_type"] = "pubmed"
    clinical_trials_df["article_type"] = "clinical_trials"
    clinical_trials_df = clinical_trials_df.rename(columns={"scientific_title": "title", "date": "date_mention"})
    pubmed_df = pubmed_df.rename(columns={"date": "date_mention"})

    return drugs_df, pubmed_df, clinical_trials_df


def aggregate_df(drugs_df, pubmed_df, clinical_trials_df):
    pubmed_mention_df = join_drugs_and_title(drugs_df, pubmed_df)
    clinical_mention_df = join_drugs_and_title(drugs_df, clinical_trials_df)
    clinical_and_pubmed_mention_df = pd.concat([pubmed_mention_df, clinical_mention_df]).reset_index(drop=True)
    journal_mention_df = clinical_and_pubmed_mention_df[
        ["atccode", "drug", "date_mention", "journal"]].drop_duplicates().reset_index(
        drop=True)
    all_mention_df = pd.concat([pubmed_mention_df, clinical_mention_df, journal_mention_df]).reset_index(drop=True)
    nested_df = all_mention_df.set_index(["atccode", 'drug'])[
        ["date_mention", "journal", "title", "article_type"]].sort_index()

    return nested_df


def generate_dict(nested_df):
    unique_index = nested_df.index.drop_duplicates()
    result_dict = []
    for index_number, index_name in zip(range(len(unique_index)), unique_index):
        intermediate_df = nested_df.loc[index_name]
        result_dict.append([{
            'atccode': index_name[0],
            'drug': index_name[1],
            'mention': [],
        }])
        for index, row in intermediate_df.iterrows():
            mention_temp_dict = {
                "date_mention": row['date_mention'].strftime("%Y/%m/%d"),
                "article_type": row["article_type"] if row['title'] is not np.NaN else "journal",
                "title": row['title'],
                "journal": row['journal']}
            result_dict[index_number][0]["mention"].append(mention_temp_dict)

    return result_dict


def write_to_json(result_dict):
    with open('result.json', 'w') as json_file:
        json.dump(result_dict, json_file, ensure_ascii=False)


def journal_with_max_distinct_drugs():
    with open("result.json") as data_file:
        data = json.load(data_file)
    print(data)

if __name__ == "__main__":
    #journal_with_max_distinct_drugs()
    main()
