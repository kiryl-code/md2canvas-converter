from models.criteria import Criteria


class CriteriaRepository:
    def __init__(self, connection_getter, db_path):
        self.connection_getter = connection_getter
        self.db_path = db_path

    def get_criteria_for_assignment(self, course_id):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM criteria WHERE assignment_id = ?"
            cursor = connection.execute(statement, (course_id,))
            rows = cursor.fetchall()
            return [Criteria(id=r["id"], assignment_id=r["assignment_id"], criteria=r["criteria"], pass_text=r["pass_text"], fail_text=r["fail_text"]) for r in rows]

    def add_criteria(self, criteria: Criteria):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "INSERT INTO criteria (assignment_id, criteria, pass_text, fail_text) VALUES (?, ?, ?, ?)",
                (criteria.assignment_id, criteria.criteria, criteria.pass_text, criteria.fail_text)
            )

    def delete_criteria(self, criteria_id):
        with self.connection_getter(self.db_path) as connection:
            connection.execute("DELETE FROM criteria WHERE id = ?", (criteria_id,))

    def update_criteria(self, criteria: Criteria):
        with self.connection_getter(self.db_path) as connection:
            connection.execute(
                "UPDATE criteria SET criteria = ?, pass_text = ?, fail_text = ? WHERE id = ?",
                (criteria.criteria, criteria.pass_text, criteria.fail_text, criteria.id)
            )

    def get_criteria(self, criteria_id):
        with self.connection_getter(self.db_path) as connection:
            statement = "SELECT * FROM criteria WHERE id = ?"
            cursor = connection.execute(statement, (criteria_id,))
            r = cursor.fetchone()
            return Criteria(id=r["id"], assignment_id=r["assignment_id"], criteria=r["criteria"], pass_text=r["pass_text"], fail_text=r["fail_text"])
