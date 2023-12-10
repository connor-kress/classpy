import tkinter as tk
from tkinter import ttk
import asyncio
import threading

from classpy import *


class CourseQueryGUI:
    def setup(self) -> None:
        # Initialize window
        root = tk.Tk()
        self.root = root
        root.title("Course Query")

        # set input widgets and entry types
        category_label = tk.Label(root, text="Category")
        self.category_combobox = tk.Entry(root)

        term_label = tk.Label(root, text="Term")
        self.term_combobox = tk.Entry(root)

        course_code_label = tk.Label(root, text="Course Code")
        self.course_code_entry = tk.Entry(root)

        course_title_label = tk.Label(root, text="Course Title")
        self.course_title_entry = tk.Entry(root)

        class_num_label = tk.Label(root, text="Class Number")
        self.class_num_entry = tk.Entry(root)

        instructor_label = tk.Label(root, text="Instructor")
        self.instructor_entry = tk.Entry(root)

        program_level_label = tk.Label(root, text="Program Level")
        self.program_level_combobox = tk.Entry(root)

        department_label = tk.Label(root, text="Department")
        self.department_entry = tk.Entry(root)

        search_button = tk.Button(root, text="Search", command=on_search_click)

        # treeview columns (without Classes attributes)
        columns = ('course number', 'title', 'description', 'credits',
                'department', 'requirements', 'fees', 'EEP_eligible', 'gen_ed')

        # display the attributes
        results_tree = ttk.Treeview(root, columns=columns, show='headings')
        self.results_tree = results_tree
        for col in columns:
            results_tree.heading(col, text=col.capitalize())
            results_tree.column(col, width=150, anchor='center')

        # scrollbar and display sizes
        h_scrollbar = ttk.Scrollbar(root, orient='horizontal', command=results_tree.xview)
        results_tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.grid(row=10, column=0, columnspan=3, sticky='ew')

        scrollbar = ttk.Scrollbar(root, orient='vertical', command=results_tree.yview)
        results_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=9, column=3, sticky='ns')

        # set the TreeView layout
        results_tree.grid(row=9, column=0, columnspan=2, sticky='nsew')

        # TreeView bind selection
        results_tree.bind('<<TreeviewSelect>>', show_course_details)

        # set the input layouts
        category_label.grid(row=0, column=0)
        self.category_combobox.grid(row=0, column=1)

        term_label.grid(row=1, column=0)
        self.term_combobox.grid(row=1, column=1)

        course_code_label.grid(row=2, column=0)
        self.course_code_entry.grid(row=2, column=1)

        course_title_label.grid(row=3, column=0)
        self.course_title_entry.grid(row=3, column=1)

        class_num_label.grid(row=4, column=0)
        self.class_num_entry.grid(row=4, column=1)

        instructor_label.grid(row=5, column=0)
        self.instructor_entry.grid(row=5, column=1)

        program_level_label.grid(row=6, column=0)
        self.program_level_combobox.grid(row=6, column=1)

        department_label.grid(row=7, column=0)
        self.department_entry.grid(row=7, column=1)

        search_button.grid(row=8, column=0, columnspan=2)


__gui = CourseQueryGUI()


def threaded_course_query():
    """Collects inputs and makes a course query."""
    category = __gui.category_combobox.get() or DEFAULT_CATEGORY
    term = __gui.term_combobox.get() or DEFAULT_TERM
    code = __gui.course_code_entry.get() or None
    title = __gui.course_title_entry.get() or None
    class_num = __gui.class_num_entry.get() or None
    instructor = __gui.instructor_entry.get() or None
    program_level = __gui.program_level_combobox.get() or None
    department = __gui.department_entry.get() or None

    result = asyncio.run(course_query(
        category=category,
        term=term,
        code=code,
        title=title,
        class_num=class_num,
        instructor=instructor,
        program_level=program_level,
        department=department,
    ))
    for course in result:
        add_course_to_treeview(__gui.results_tree, course)


def add_course_to_treeview(tree: ttk.Treeview, course: Course):
    """Adds a `Course` to the GUI's treeview."""
    gen_ed_str = ', '.join(course.gen_ed) if course.gen_ed else 'N/A'
    fees_str = f'${course.fees:.2f}' if course.fees else 'N/A'

    # concatenating class/session information
    class_details = ''
    for class_obj in course.available_classes:
        class_detail = (
            f'Number: {class_obj.number}, '
            f'Instructors: {', '.join(class_obj.instructors) if
                            class_obj.instructors else 'none'}, '
            f'Online: {'Yes' if class_obj.is_online else 'No'}, '
        )
        if class_obj.final_exam_time:
            class_detail += (
                f'Exam Time: {class_obj.final_exam_time[0].strftime('%Y-%m-%d %H:%M')} '
                f'to {class_obj.final_exam_time[1].strftime('%Y-%m-%d %H:%M')}, '
            )
        class_detail += (
            f'Dates: {class_obj.class_dates[0].strftime('%Y-%m-%d')} to '
                f'{class_obj.class_dates[1].strftime('%Y-%m-%d')}, '
            f'Classrooms: {', '.join(room.code for room in class_obj.classrooms)}'
        )
        class_details += class_detail + '\n'
    class_details.removesuffix('\n')

    # insert the course info into the treeview
    tree.insert('', 'end', values=(
        course.number,
        course.title,
        course.description,
        course.credits,
        course.department,
        str(course.requirements.expr) if course.requirements.expr is not None
            else course.requirements.string,
        fees_str,
        'Yes' if course.EEP_eligable else 'No',
        gen_ed_str,
        class_details,
    ))


def on_search_click():
    """Runs a course query on a new thread."""
    thread = threading.Thread(target=threaded_course_query)
    thread.start()


def show_course_details(_event):
    """Shows more in depth details for a course in a pop-up."""
    selected_item = __gui.results_tree.selection()[0]
    course = __gui.results_tree.item(selected_item, 'values')
    detailed_info = f'Course Number: {course[0]}\nTitle: '\
                    f'{course[1]}\nDescription: {course[2]}\n'\
                    f'Requirement: {course[5]}\nSessions: {course[9]}'
    detail_window = tk.Toplevel(__gui.root)
    detail_window.title("Course Details")
    tk.Label(detail_window, text=detailed_info).pack()


def main() -> None:
    __gui.setup()
    __gui.root.mainloop()


if __name__ == '__main__':
    main()
