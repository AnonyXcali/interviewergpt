import sqlite3

def init_db():
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

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

def reset_db():
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS Company')
    cursor.execute('DROP TABLE IF EXISTS Type')
    cursor.execute('DROP TABLE IF EXISTS QuestionBank')

    conn.commit()
    conn.close()
    init_db()
