from flask import Blueprint, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import sqlite3
import json
import time

from .database import add_company, add_type, add_question, get_questions_by_field, reset_db
from .openai_service import get_openai_response, get_openai_response_stream

bp = Blueprint('routes', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}})

@bp.route('/add-question', methods=['POST'])
def add_question_endpoint():
    data = request.json
    company_id = add_company(data['company'])
    type_id = add_type(data['type'])

    if 'custom_solution' in data:
        prompt = f"""
        The following prompt requires you to update your memory - 
        Here is a new interview question for the {data['company']} company, for a {data['type']} position:
        {data['description']} and {data['custom_solution']} solution

        NOTE -  Algorithm's Application Score or AAS is the score by which one can determine the extent of 
        usability of the optimized solution's algorithm across multiple questions which may or may not differ
        by type of coding question. Score ranges from 1 to 10 where the particular solution in context which you
        would provide with highers score means it can be used in a generic or modified way with other questions.
        Please assume at your suitable best.

        Please provide the following:
        1. An optimized solution.
        2. Questions to be asked before attempting the question.
        3. Algorithm's Application Score (AAS) for the optimized solution.
        4. Similar interview questions.
        5. A difficulty score from 0 to 10, where higher is more difficult.
        6. [OPTIONAL IF SOLUTION IS ALREADY OPTIMIZED] Point out caveats or shortcomings for the provided solution
        7. A JSON structure containing the following keys title, type, optimized_solution, AAS, similar (Array of titles of similar interview questions),
        difficulty.
        """
    else:
        prompt = f"""
        The following prompt requires you to update your memory - 
        Here is a new interview question for the {data['company']} company, for a {data['type']} position:
        {data['description']}

        NOTE -  Algorithm's Application Score or AAS is the score by which one can determine the extent of 
        usability of the optimized solution's algorithm across multiple questions which may or may not differ
        by type of coding question. Score ranges from 1 to 10 where the particular solution in context which you
        would provide with highers score means it can be used in a generic or modified way with other questions.
        Please assume at your suitable best.

        Please provide the following:
        1. An optimized solution.
        2. Questions to be asked before attempting the question.
        3. Algorithm's Application Score (AAS) for the optimized solution.
        4. Similar interview questions.
        5. A difficulty score from 0 to 10, where higher is more difficult.
        6. A JSON structure containing the following keys title, type, optimized_solution, AAS, similar (Array of titles of similar interview questions),
        difficulty.

        """

    openai_response = get_openai_response(prompt)
    print(openai_response)
    optimized_solution = openai_response['choices'][0]['message']['content']
    aas = 7  # Placeholder value, replace with actual logic to compute AAS
    difficulty_score = 5  # Placeholder value, replace with actual logic to compute difficulty score

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

    def generate_response():
        for chunk in get_openai_response_stream(prompt):
            yield f"data: {chunk}\n\n"

    return Response(stream_with_context(generate_response()), mimetype='text/event-stream')

@bp.route('/stream-query', methods=['GET'])
def stream_query():
    prompt = request.args.get('query')
    return get_openai_response_stream(prompt)
# @bp.route('/stream-query', methods=['GET'])
# def stream_query():
#     prompt = request.args.get('prompt')
#     if not prompt:
#         return jsonify({"status": "error", "message": "Prompt not provided"}), 400

#     def generate():
#         for chunk in get_openai_response_stream(prompt):
#             yield f"data: {chunk}\n\n"
#         yield "event: end\ndata: end\n\n"

#     return Response(stream_with_context(generate()), mimetype='text/event-stream')

# @bp.route('/stream-query', methods=['GET'])
# def stream_query():
#     prompt = request.args.get('prompt')
#     if not prompt:
#         return jsonify({"status": "error", "message": "Prompt not provided"}), 400

#     def generate():
#         try:
#             for chunk in get_openai_response_stream(prompt):
#                 if chunk.strip():  # Check if chunk is not empty
#                     try:
#                         chunk_data = json.loads(chunk)
#                         if 'choices' in chunk_data and len(chunk_data['choices']) > 0 and 'delta' in chunk_data['choices'][0]:
#                             content = chunk_data['choices'][0]['delta'].get('content', '')
#                             if content:
#                                 yield f"data: {content}\n\n"
#                     except json.JSONDecodeError as e:
#                         print(f"Error decoding JSON: {e}")
#                         yield f"data: Error decoding JSON: {e}\n\n"
#                         continue
#             yield "event: end\ndata: end\n\n"
#         except Exception as e:
#             print(f"Error in stream-query generate function: {e}")
#             yield f"data: Error in stream-query generate function: {e}\n\n"

#     return Response(stream_with_context(generate()), mimetype='text/event-stream')

# @bp.route('/stream-query', methods=['GET'])
# def stream_query():
#     def generate():
#         for i in range(5):
#             yield f"data: Message {i+1}\n\n"
#             time.sleep(1)
#         yield "event: end\ndata: end\n\n"

#     return Response(stream_with_context(generate()), mimetype='text/event-stream')


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
