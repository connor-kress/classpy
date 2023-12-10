import pandas as pd

from ..data.raw_data import (
    PROFESSORS_PATH,
    PROFESSORS_CLEANED_PATH,
)

def clean_professor_data() -> None:
    # load the dataset
    data = pd.read_csv(PROFESSORS_PATH)

    # replace 'None' with Na for consistency
    data.replace('None', pd.NA, inplace=True)

    # remove rows with at least four Na values (did not find in ratemyprofessor)
    data_cleaned = data.dropna(thresh=data.shape[1] - 3)

    # remove rows where 'num_ratings' is 0 (found but no rating)
    data_cleaned = data_cleaned[data_cleaned['num_ratings'] != 0]

    # convert would_take_again percentage to float
    data_cleaned['would_take_again'] = data_cleaned['would_take_again'].str.rstrip('%').astype('float') / 100


    # imputation method for missing would_take_again data with mean
    mean_num_ratings = data_cleaned['would_take_again'].mean()
    data_cleaned['would_take_again'].fillna(mean_num_ratings, inplace=True)


    # normalizing rating_value and num_ratings
    max_num_ratings = data_cleaned['num_ratings'].max()
    data_cleaned['normalized_rating_value'] = (data_cleaned['rating_value'] / 5)
    data_cleaned['normalized_num_ratings'] = (data_cleaned['num_ratings'] / max_num_ratings)

    # calculating the score
    # weight: 40% for normalized rating, 40% for normalized number of ratings, 20% for would take again percentage
    data_cleaned['score'] = 0.4 * data_cleaned['normalized_rating_value'] \
                          + 0.4 * data_cleaned['normalized_num_ratings'] \
                          + 0.2 * data_cleaned['would_take_again']

    # sorting the data by the new score
    # round to 2 decimal places
    data_cleaned_sorted = data_cleaned.sort_values(by='score', ascending=False).round(2)

    # storing the cleaned data
    data_cleaned_sorted.to_csv(PROFESSORS_CLEANED_PATH, index=False)
