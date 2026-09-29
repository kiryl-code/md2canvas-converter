from models.assignment import Assignment


class AssignmentsRepository:
    def __init__(self, connection_getter, db_path):
        self.connection_getter = connection_getter
        self.db_path = db_path

    def get_assignments_for_course(self, course_id):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM assignments WHERE course_id = ?"
            cursor = connection.execute(statement, (course_id,))
            rows = cursor.fetchall()
            return [Assignment(id=r["id"], course_id=r["course_id"], name=r["name"], introduction_template=r["introduction_template"]) for r in rows]

    def add_assignment(self, assignment):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "INSERT INTO assignments (course_id, name, introduction_template) VALUES (?, ?, ?)",
                (assignment.course_id, assignment.name, assignment.introduction_template)
            )

    def delete_assignment(self, assignment_id):
        with self.connection_getter(self.db_path) as connection:
            connection.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))

    def update_assignment(self, assignment):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "UPDATE assignments SET name = ?, introduction_template = ? WHERE id = ?",
                (assignment.name, assignment.introduction_template, assignment.id)
            )

    def get_assignment(self, assignment_id):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM assignments WHERE id = ?"
            cursor = connection.execute(statement, (assignment_id,))
            row = cursor.fetchone()
            return Assignment(id=row["id"], course_id=row["course_id"], name=row["name"], introduction_template=row["introduction_template"])
