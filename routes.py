from flask import Blueprint, request, jsonify
from app.models import add_company, add_type, add_question, get_questions_by_type, get_questions_by_company, get_questions_by_difficulty
from app.db import reset_db

routes = Blueprint('routes', __name__)

@routes.route('/add-question', methods=['POST'])
def add_question_endpoint():
    data = request.json
    company_id = add_company(data['company'])
    type_id = add_type(data['type'])

    # Generate a prompt for GPT-4o to process
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

@routes.route('/questions/type/<type_name>', methods=['GET'])
def get_questions_by_type_endpoint(type_name):
    questions = get_questions_by_type(type_name)
    return jsonify(questions)

@routes.route('/questions/company/<company_name>', methods=['GET'])
def get_questions_by_company_endpoint(company_name):
    questions = get_questions_by_company(company_name)
    return jsonify(questions)

@routes.route('/questions/difficulty/<int:difficulty_score>', methods=['GET'])
def get_questions_by_difficulty_endpoint(difficulty_score):
    questions = get_questions_by_difficulty(difficulty_score)
    return jsonify(questions)

@routes.route('/reset-db', methods=['POST'])
def reset_db_endpoint():
    reset_db()
    return jsonify({"status": "success", "message": "Database reset successfully"}), 200
s