CREATE_COURSES_TABLE = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code VARCHAR(6) NOT NULL UNIQUE,
        name TEXT NOT NULL,
        directory TEXT NOT NULL,
        is_archived BOOLEAN NOT NULL
    )
    """

CREATE_ASSIGNMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        introduction_template TEXT NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    """

CREATE_CRITERIA_TABLE = """
    CREATE TABLE IF NOT EXISTS criteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        criteria TEXT NOT NULL,
        pass_text TEXT NOT NULL,
        fail_text TEXT NOT NULL,
        FOREIGN KEY (assignment_id) REFERENCES assignments (id) ON DELETE CASCADE
    )
    """

CREATE_FEEDBACK_TABLE = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        student_id VARCHAR(9) NOT NULL,
        student_name TEXT NOT NULL,
        grade TEXT NOT NULL,
        criteria TEXT NOT NULL,
        extra_comment TEXT NOT NULL,
        feedback TEXT NOT NULL,
        FOREIGN KEY (assignment_id) REFERENCES assignment (id) ON DELETE CASCADE
    )
    """