import matplotlib.pyplot as plt
import pandas as pd

from classpy import COURSE_TITLES_PATH


def main() -> None:
    # load the csv data into a dataframe
    courses = pd.read_csv(COURSE_TITLES_PATH)

    # Meeting type pychart
    meeting_type_counts = courses['Meet'].value_counts()
    plt.pie(meeting_type_counts,
            labels=meeting_type_counts.index,
            autopct='%1.1f%%',
            textprops={'fontsize': 10})
    plt.title('Meeting Type Distribution')
    legend_labels = [f'{label} - {percentage:.1f}%' for label, percentage in
                     zip(meeting_type_counts.index,
                         meeting_type_counts/meeting_type_counts.sum()*100)]
    plt.legend(legend_labels, bbox_to_anchor=(0.3, 0.15))
    plt.show()
    plt.close()


    department_counts = courses['Department'].value_counts()
    # Get the top 10 departments
    top_10_departments = department_counts.head(10)
    plt.figure(figsize=(40, 10))
    plt.title('Top 10 Departments by Number of Courses')
    plt.barh(top_10_departments.index, top_10_departments.values)
    plt.xlabel('Number of Courses')
    plt.ylabel('Department')
    plt.gca().invert_yaxis()  # puts top departments at the top
    plt.show()
    plt.close()

    instructor_course_counts = courses['Instructor'].value_counts().head(10)
    plt.figure(figsize=(15, 5))
    plt.title('Top 10 Instructors by Number of Courses')
    plt.barh(instructor_course_counts.index,
             instructor_course_counts.values)
    plt.xlabel('Number of Courses')
    plt.ylabel('Instructor')
    plt.gca().invert_yaxis()  # puts top instructors at the top
    plt.show()
    plt.close()


if __name__ == '__main__':
    main()
