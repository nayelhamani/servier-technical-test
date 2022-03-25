from utils.utils import read_csv, lower_df, format_date, join_drugs_and_title
import pandas as pd


def main():
    start_pipeline()


def start_pipeline():
    drugs_df, pubmed_df, clinical_trials_df = get_csv()
    drugs_df, pubmed_df, clinical_trials_df = process_csv(drugs_df, pubmed_df, clinical_trials_df)
    joins(drugs_df, pubmed_df, clinical_trials_df)


def get_csv():
    clinical_trials_df = read_csv("ressources/clinical_trials.csv")
    drugs_df = read_csv("ressources/drugs.csv")
    pubmed_df = read_csv("ressources/pubmed.csv")
    return drugs_df, pubmed_df, clinical_trials_df


def process_csv(drugs_df, pubmed_df, clinical_trials_df):
    #lower str column
    drugs_df = lower_df(drugs_df)
    pubmed_df = lower_df(pubmed_df)
    clinical_trials_df = lower_df(clinical_trials_df)

    #format date
    pubmed_df = format_date(pubmed_df, "date")
    clinical_trials_df = format_date(clinical_trials_df, "date")
    return drugs_df, pubmed_df, clinical_trials_df


def joins(drugs_df, pubmed_df, clinical_trials_df):
    pubmed_mention_df = join_drugs_and_title(drugs_df, pubmed_df, "title")
    clinical_mention_df = join_drugs_and_title(drugs_df, clinical_trials_df, "scientific_title")
    print(pubmed_mention_df)
    print(clinical_mention_df)

    all_mentions_df = pd.concat([pubmed_mention_df, clinical_mention_df]).reset_index(drop=True)
    print(all_mentions_df)
    print(all_mentions_df.columns)
    journal_mention_df = all_mentions_df[["drug", "date", "journal"]].drop_duplicates().reset_index(drop=True)
    print(journal_mention_df)



if __name__ == "__main__":
    main()
