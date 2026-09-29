import sqlite3

from database.statements import CREATE_ASSIGNMENTS_TABLE, CREATE_COURSES_TABLE, CREATE_CRITERIA_TABLE, \
    CREATE_FEEDBACK_TABLE


def get_connection(path: str):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init(path: str):
    connection = get_connection(path)
    cursor = connection.cursor()

    cursor.execute(CREATE_COURSES_TABLE)
    cursor.execute(CREATE_ASSIGNMENTS_TABLE)
    cursor.execute(CREATE_CRITERIA_TABLE)
    cursor.execute(CREATE_FEEDBACK_TABLE)

    connection.commit()
    connection.close()
