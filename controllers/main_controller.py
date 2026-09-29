from tkinter import messagebox

from controllers.utils import check_if_directory_exists_and_create, save_md_file
from converter.converter import convert
from database import assignments_repository
from database.assignments_repository import AssignmentsRepository
from database.database import get_connection
from gui.main_window import CanvasConverterGui
from gui.views.create_assignment_view import CreateAssignmentView
from gui.views.create_criteria_view import CreateCriteriaView
from gui.views.feedback_preview import FeedbackPreview
from gui.views.file_converter import FileConverter
from models.assignment import Assignment
from models.course import Course
from database.course_repository import CoursesRepository
from gui.views.create_course_view import CreateCourseView
from database.criteria_repository import CriteriaRepository
from models.criteria import Criteria


class MainController:
    def __init__(self, root, db_path: str):
        self.selected_assignment: Assignment | None = None
        self.root = root
        self.main_window = CanvasConverterGui(root, self)
        self.main_window.pack(fill="both", expand=True)
        self.selected_course: Course | None = None
        self.show_archived = False
        self.courses_repository = CoursesRepository(get_connection, db_path)
        self.assignments_repository = AssignmentsRepository(get_connection, db_path)
        self.criteria_repository = CriteriaRepository(get_connection, db_path)
        self.render_courses()
        self.current_feedback = str()


    def render_courses(self):
        courses = self.courses_repository.get_courses(self.show_archived)
        filtered_courses = [course for course in courses if course.is_archived == self.show_archived]
        selected_course_id = self.selected_course.id if self.selected_course else None
        self.main_window.courses_panel.render_courses(filtered_courses, self.show_archived)

    def create_course_on_click(self, course = None):
        CreateCourseView(self.main_window, self.on_course_save, course)

    def on_course_save(self, course):
        if course.id and self.courses_repository.get_course(course.id):
            self.courses_repository.update_course(course)
        else:
            self.courses_repository.add_course(course)
        self.render_courses()

    def archive_course(self, course):
        course.is_archived = True
        self.courses_repository.update_course(course)
        self.render_courses()

    def unarchive_course(self, course):
        course.is_archived = False
        self.courses_repository.update_course(course)
        self.render_courses()

    def file_converter_on_click(self):
        FileConverter(self.root, self.on_file_converter_export)

    def on_file_converter_export(self, input_file, export_directory):
        convert(input_file, export_directory, "styles/kiya-pages-style.css")

    def toggle_archived(self):
        self.show_archived = not self.show_archived
        if self.show_archived:
            self.main_window.courses_panel.archived_courses_button.configure(text="Aktiva kurser")
            self.main_window.courses_panel.title_label.configure(text="Arkiverade kurser")
        else:
            self.main_window.courses_panel.archived_courses_button.configure(text="Arkiverade kurser")
            self.main_window.courses_panel.title_label.configure(text="Kurser")
        self.render_courses()

    def select_course(self, course_id):
        course = self.courses_repository.get_course(course_id)
        self.selected_course = course
        self.render_assignments()
        self.main_window.main_area.evaluation_frame.reset()

    def render_assignments(self):
        if self.selected_course:
            assignments = self.assignments_repository.get_assignments_for_course(self.selected_course.id)
            self.main_window.main_area.assignments.render_assignments(assignments)
        else:
            self.main_window.main_area.assignments.render_assignments([])

    def create_assignment_on_click(self, assignment = None):
        if not self.selected_course:
            messagebox.showwarning("Ingen kurs vald", "Välj en kurs först")
            return
        CreateAssignmentView(self.main_window, self.selected_course.id, self.on_assignment_save, assignment)

    def on_assignment_save(self, assignment):
        if assignment and assignment.id and self.assignments_repository.get_assignment(assignment.id):
            self.assignments_repository.update_assignment(assignment)
            if assignment.id == self.selected_assignment.id:
                self.selected_assignment = self.assignments_repository.get_assignment(assignment.id)
        else:
            self.assignments_repository.add_assignment(assignment)
        self.render_assignments()

    def select_assignment(self, assignment_id: int):
        if not self.selected_course:
            return
        assignment = self.assignments_repository.get_assignment(assignment_id)
        self.selected_assignment = assignment if assignment else None
        self.render_assignments()
        self.render_main_area()

    def render_main_area(self):
        criteria_list = self.criteria_repository.get_criteria_for_assignment(self.selected_assignment.id) if self.selected_assignment else []
        self.main_window.main_area.evaluation_frame.render_criteria(criteria_list)

    def create_criteria_on_click(self, criteria = None):
        if not self.selected_assignment:
            messagebox.showwarning("Ingen uppgift vald", "Välj en uppgift först")
            return
        CreateCriteriaView(self.main_window, self.selected_assignment.id, criteria, self.on_criteria_save)

    def on_criteria_save(self, criteria):
        if criteria and criteria.id and self.criteria_repository.get_criteria(criteria.id):
            self.criteria_repository.update_criteria(criteria)
        else:
            self.criteria_repository.add_criteria(criteria)
        self.render_main_area()

    def delete_criteria_on_click(self, criteria_id):
        self.criteria_repository.delete_criteria(criteria_id)
        self.render_main_area()

    def delete_assignment(self, assignment_id):
        self.assignments_repository.delete_assignment(assignment_id)
        if assignment_id == self.selected_assignment.id:
            self.selected_assignment = None
        self.render_assignments()
        self.render_main_area()

    def preview_feedback_on_click(self, criteria_data, student_name, grade, additional_comment=""):
        if not self.selected_assignment:
            messagebox.showwarning("Ingen uppgift vald", "Välje en uppgift först")
            return
        self.compile_feedback(criteria_data, self.selected_assignment.introduction_template, student_name, grade, additional_comment)
        FeedbackPreview(self.main_window, self.current_feedback, self.preview_feedback_on_save)

    def preview_feedback_on_save(self, feedback):
        self.current_feedback = feedback

    def export_feedback_on_click(self, student_id):
        if not self.selected_course or not self.selected_assignment:
            messagebox.showwarning("Ingen kurs / uppgift vald", "Välj en kurs / uppgift först")
            return
        if not student_id:
            messagebox.showwarning("Studenid saknas", "Ange studentid")
            return
        file_path = f"{self.selected_course.directory}/{self.selected_assignment.name}"
        check_if_directory_exists_and_create(file_path)
        check_if_directory_exists_and_create(f"{file_path}/html")
        md_path = save_md_file(file_path, student_id, self.current_feedback)
        output_path = f"{file_path}/html/"
        convert(md_path, output_path, "styles/kiya-feedback-style.css")

    def compile_feedback(self, criteria_data, intro, student_name, grade, additional_comment=""):
        self.current_feedback = str()

        intro = intro.replace("{{name}}", student_name)
        intro = intro.replace("{{grade}}", grade)

        self.current_feedback += intro
        self.current_feedback += "\n\n----\n\n"

        for c_d in criteria_data:
            self.current_feedback += f"{c_d}\n\n"

        self.current_feedback += f"\n{additional_comment}"

    def reset_feedback(self):
        self.current_feedback = str()
