import sqlite3

CONN = sqlite3.connect('language_categories.db')
CURSOR = CONN.cursor()

def execute_and_commit(sql, parameters =()):
    """ Execute an SQL script and commit the changes to the database. """
    CURSOR.execute(sql, parameters)
    CONN.commit()
