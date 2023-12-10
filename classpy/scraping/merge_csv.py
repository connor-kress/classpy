import pandas as pd

from ..data.raw_data import (
    COURSE_TITLES_PATH,
    PROFESSORS_CLEANED_PATH,
    COURSE_WITH_SCORE_PATH,
)


def _find_matching_score(course_row: pd.DataFrame, professors: pd.DataFrame) -> float:
    # check if the instructor name is a string
    if not isinstance(course_row['Instructor'], str):
        return pd.NA

    course_instructor = course_row['Instructor'].strip().lower()
    course_department = course_row['Department'].lower()

    # filter the professors dataframe for rows with the same instructor
    matching_professors = professors[professors['Instructor'].str.lower().str.strip() == course_instructor]

    # if no matching instructors, return NaN
    if matching_professors.empty:
        return pd.NA

    # if instructor is associated with only one department
    if matching_professors['Department'].nunique() == 1:
        return matching_professors.iloc[0]['score']

    # if instructor is associated with multiple departments
    else:
        # compare department names and find the closest match
        for _, prof_row in matching_professors.iterrows():
            prof_department = prof_row['Department'].lower().replace('department', '') # take out 'department' for correctness
            if course_department in prof_department or prof_department in course_department:
                return prof_row['score']

        # if no department names match closely, return NaN
        return pd.NA


def merge_score_data() -> None:
    # load the data from CSV files
    course_titles = pd.read_csv(COURSE_TITLES_PATH)
    professors_cleaned = pd.read_csv(PROFESSORS_CLEANED_PATH)

    # apply the function to each row in the course_titles
    course_titles['Score'] = course_titles.apply(
        lambda row: _find_matching_score(row, professors_cleaned),
        axis=1
    )

    # imputation method for NA score
    mean_ratings = course_titles['Score'].mean().round(2)
    course_titles['Score'].fillna(mean_ratings, inplace=True)

    # save the updated DataFrame
    course_titles.to_csv(COURSE_WITH_SCORE_PATH, index=False)
