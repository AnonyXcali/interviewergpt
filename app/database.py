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
            description TEXT UNIQUE NOT NULL,
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

def add_company(name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Company (name) VALUES (?)', (name,))
    cursor.execute('SELECT id FROM Company WHERE name = ?', (name,))
    company_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return company_id

def add_type(name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Type (name) VALUES (?)', (name,))
    cursor.execute('SELECT id FROM Type WHERE name = ?', (name,))
    type_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return type_id

def add_question(company_id, type_id, aas, description, difficulty_score):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO QuestionBank (company_id, type_id, aas, description, difficulty_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_id, type_id, aas, description, difficulty_score))
    conn.commit()
    conn.close()

def get_questions_by_field(field, value):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
        FROM QuestionBank
        JOIN Company ON QuestionBank.company_id = Company.id
        JOIN Type ON QuestionBank.type_id = Type.id
        WHERE {field} = ?
    ''', (value,))
    questions = cursor.fetchall()
    conn.close()
    return questions
