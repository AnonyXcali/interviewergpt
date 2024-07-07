from flask import Blueprint, request, jsonify, Response
from .database import init_db, reset_db, add_company, add_type, add_question, get_questions_by_field
from .openai_service import get_openai_response
import sqlite3

bp = Blueprint('routes', __name__)

@bp.route('/add-question', methods=['POST'])
def add_question_endpoint():
    data = request.json
    company_id = add_company(data['company'])
    type_id = add_type(data['type'])

    # Generate a prompt for GPT-4o to process
    if 'custom_solution' in data:
        prompt = f"""
        The following prompt requires you to update your memory - 
        Here is a new interview question for the {data['company']} company, for a {data['type']} position:
        {data['description']} and {data['custom_solution']} solution
        
        Please provide the following:
        1. An optimized solution.
        2. Questions to be asked before attempting the question.
        3. Algorithm's Application Score (AAS) for the optimized solution.
        4. Similar interview questions.
        5. A difficulty score from 0 to 10, where higher is more difficult.
        6. [OPTIONAL IF SOLUTION IS ALREADY OPTIMIZED] Point out caveats or shortcomings for the provided solution
        """
    else:
        prompt = f"""
        The following prompt requires you to update your memory - 
        Here is a new interview question for the {data['company']} company, for a {data['type']} position:
        {data['description']}
        
        Please provide the following:
        1. An optimized solution.
        2. Questions to be asked before attempting the question.
        3. Algorithm's Application Score (AAS) for the optimized solution.
        4. Similar interview questions.
        5. A difficulty score from 0 to 10, where higher is more difficult.
        """

    # Get GPT-4o response
    openai_response = get_openai_response(prompt)

    # Extract the necessary information from the response
    optimized_solution = openai_response['choices'][0]['message']['content']
    # Additional parsing and processing as needed...

    # Example: extracting details (this would need proper parsing based on response format)
    aas = 7  # This would be extracted from the response
    difficulty_score = 5  # This would be extracted from the response

    # Add question to the database
    add_question(company_id, type_id, aas, data['description'], difficulty_score)

    return jsonify({"status": "success", "optimized_solution": optimized_solution}), 201

@bp.route('/questions/type/<type_name>', methods=['GET'])
def get_questions_by_type(type_name):
    questions = get_questions_by_field('Type', type_name)
    return jsonify(questions)

@bp.route('/questions/company/<company_name>', methods=['GET'])
def get_questions_by_company(company_name):
    questions = get_questions_by_field('Company', company_name)
    return jsonify(questions)

@bp.route('/questions/difficulty/<int:difficulty_score>', methods=['GET'])
def get_questions_by_difficulty(difficulty_score):
    questions = get_questions_by_field('difficulty_score', difficulty_score)
    return jsonify(questions)

@bp.route('/reset-db', methods=['POST'])
def reset_db_endpoint():
    reset_db()
    return jsonify({"status": "success", "message": "Database reset successfully"}), 200

@bp.route('/query', methods=['POST'])
def general_query():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"status": "error", "message": "Prompt not provided"}), 400

    openai_response = get_openai_response(prompt)
    return jsonify(openai_response)

@bp.route('/stream-questions', methods=['GET'])
def stream_questions():
    def generate():
        conn = sqlite3.connect('interview_helper.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
            FROM QuestionBank
            JOIN Company ON QuestionBank.company_id = Company.id
            JOIN Type ON QuestionBank.type_id = Type.id
        ''')
        for row in cursor.fetchall():
            yield f"{row}\n"
        conn.close()

    return Response(generate(), mimetype='text/plain')

@bp.route('/search-questions', methods=['GET'])
def search_questions():
    query = request.args.get('query')
    if not query:
        return jsonify({"status": "error", "message": "Query not provided"}), 400

    conn = sqlite3.connect('interview_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT QuestionBank.description, Company.name, Type.name, QuestionBank.aas, QuestionBank.difficulty_score
        FROM QuestionBank
        JOIN Company ON QuestionBank.company_id = Company.id
        JOIN Type ON QuestionBank.type_id = Type.id
        WHERE QuestionBank.description LIKE ?
    ''', ('%' + query + '%',))
    questions = cursor.fetchall()
    conn.close()
    return jsonify(questions)
