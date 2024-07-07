from flask import Flask, request, jsonify
import os
import sqlite3
import requests

app = Flask(__name__)

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = 'https://api.openai.com/v1/completions'

# Initialize SQLite database
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

init_db()

# Function to add a company to the database
def add_company(name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Company (name) VALUES (?)', (name,))
    cursor.execute('SELECT id FROM Company WHERE name = ?', (name,))
    company_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return company_id

# Function to add a type to the database
def add_type(name):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Type (name) VALUES (?)', (name,))
    cursor.execute('SELECT id FROM Type WHERE name = ?', (name,))
    type_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return type_id

# Function to add a question to the database
def add_question(company_id, type_id, aas, description, difficulty_score):
    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO QuestionBank (company_id, type_id, aas, description, difficulty_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_id, type_id, aas, description, difficulty_score))
    conn.commit()
    conn.close()

# Function to generate a response from OpenAI using GPT-4
def get_openai_response(prompt):
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a coding interview prepare assistant that helps the user to prepare for interviews for companies like FAANG."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    return response.json()

# Endpoint to add a question
@app.route('/add-question', methods=['POST'])
def add_question_endpoint():
    data = request.json
    company_id = add_company(data['company'])
    type_id = add_type(data['type'])
    
    # Generate a prompt for GPT-4 to process
    prompt = f"""
    Here is a new interview question for the {data['company']} company, for a {data['type']} position:
    {data['description']}
    
    Please provide the following:
    1. An optimized solution.
    2. Questions to be asked before attempting the question.
    3. Algorithm's Application Score (AAS) for the optimized solution.
    4. Similar interview questions.
    5. A difficulty score from 0 to 10, where higher is more difficult.
    """
    
    # Get GPT-4 response
    openai_response = get_openai_response(prompt)
    print(openai_response)
    
    # Extract the necessary information from the response
    optimized_solution = openai_response['choices'][0]['message']['content']
    # You will need to parse the response content to extract other details
    # For simplicity, we'll assume the response contains all necessary details in the correct format
    
    # Example: extracting details (this would need proper parsing based on response format)
    aas = 7  # This would be extracted from the response
    difficulty_score = 5  # This would be extracted from the response
    
    # Add question to the database
    add_question(company_id, type_id, aas, data['description'], difficulty_score)
    
    return jsonify({"status": "success", "optimized_solution": optimized_solution}), 201

# Endpoint to retrieve questions based on type
@app.route('/questions/type/<type_name>', methods=['GET'])
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
    return jsonify(questions)

# Endpoint to retrieve questions based on company
@app.route('/questions/company/<company_name>', methods=['GET'])
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
    return jsonify(questions)

# Endpoint to retrieve questions based on difficulty
@app.route('/questions/difficulty/<int:difficulty_score>', methods=['GET'])
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
    return jsonify(questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
