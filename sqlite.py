import sqlite3

def init_db():
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()

    # Create Company table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create Type table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create QuestionBank table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionBank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            type_id INTEGER,
            aas INTEGER,
            description TEXT,
            difficulty_score INTEGER,
            FOREIGN KEY (company_id) REFERENCES Company(id),
            FOREIGN KEY (type_id) REFERENCES Type(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()
