import sqlite3

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
        INSERT INTO QuestionBank (company_id, type_id, aas, description, difficulty_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_id, type_id, aas, description, difficulty_score))
    conn.commit()
    conn.close()

def get_questions_by_type(type_name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
        FROM QuestionBank
        JOIN Company ON QuestionBank.company_id = Company.id
        JOIN Type ON QuestionBank.type_id = Type.id
        WHERE Type.name = ?
    ''', (type_name,))
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_questions_by_company(company_name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
        FROM QuestionBank
        JOIN Company ON QuestionBank.company_id = Company.id
        JOIN Type ON QuestionBank.type_id = Type.id
        WHERE Company.name = ?
    ''', (company_name,))
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_questions_by_difficulty(difficulty_score):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
        FROM QuestionBank
        JOIN Company ON QuestionBank.company_id = Company.id
        JOIN Type ON QuestionBank.type_id = Type.id
        WHERE QuestionBank.difficulty_score = ?
    ''', (difficulty_score,))
    questions = cursor.fetchall()
    conn.close()
    return questions
