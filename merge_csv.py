import pandas as pd

# load the data from CSV files
course_titles = pd.read_csv('course_titles.csv')
professors_cleaned = pd.read_csv('professors_cleaned.csv')


def find_matching_score(course_row, professors):
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

# apply the function to each row in the course_titles
course_titles['Score'] = course_titles.apply(lambda row: find_matching_score(row, professors_cleaned), axis=1)

# imputation method for NA score
mean_ratings = course_titles['Score'].mean().round(2)
course_titles['Score'].fillna(mean_ratings, inplace=True)

# save the updated DataFrame
course_with_score = 'course_with_score.csv'
course_titles.to_csv(course_with_score, index=False)

