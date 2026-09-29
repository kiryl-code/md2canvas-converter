from models.course import Course


class CoursesRepository:
    def __init__(self, connection_getter, db_path):
        self.connection_getter = connection_getter
        self.db_path = db_path

    def add_course(self, course):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "INSERT INTO courses (course_code, name, directory, is_archived) VALUES (?, ?, ?, ?)",
                (course.course_code, course.name, course.directory, course.is_archived)
            )

    def update_course(self, course):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "UPDATE courses SET course_code = ?, name = ?, directory = ?, is_archived = ? WHERE id = ?",
                (course.course_code, course.name, course.directory, course.is_archived, course.id)
            )

    def delete_course(self, course_id):
        with self.connection_getter(self.db_path) as connection:
            connection.execute("DELETE FROM courses WHERE id = ?", (course_id,))

    def get_courses(self, include_archived=False):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM courses" if include_archived else "SELECT * FROM courses WHERE is_archived = 0"
            cursor = connection.execute(statement)
            rows = cursor.fetchall()
            return [Course(id=row["id"], course_code=row["course_code"], name=row["name"], directory=row["directory"], is_archived=row["is_archived"]) for row in rows]

    def get_course(self, course_id):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM courses WHERE id = ?"
            cursor = connection.execute(statement, (course_id,))
            row = cursor.fetchone()
            return Course(id=row["id"], course_code=row["course_code"], name=row["name"], directory=row["directory"], is_archived=row["is_archived"])