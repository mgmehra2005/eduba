from flask import Blueprint, render_template, jsonify, request, json
from app import app
from app.db_connect import DBConnection
from app.eduba_engine import update_mastery, EdubaAIEngine

main = Blueprint("main", __name__)
conn = DBConnection(app.config)
aiEngine = EdubaAIEngine()

@main.route("/")
def index():
    return render_template("index.html")


# -----------------------Page Routes-----------------------
@main.route("/solution")
def solution_page():
    return render_template('response.html')

# -----------------------API Routes-----------------------

# @main.route("/concepts", methods=['GET']) 
# def concepts():
#     return jsonify(conn.get_db_cursor("select * from concepts;"))

# @main.route('/exercises/<int:concept_id>', methods=['GET'])
def exercise(concept_id):
    """
    Fetches exercises related to a specific concept_id from the database and returns them as a JSON response. Each exercise includes its id, problem text, and difficulty level.
    Expects a concept_id as a URL parameter.
    """
    if not concept_id:
        return jsonify({"error": "Invalid concept id"})
    
    query = f'select exercise_id, problem_text, difficulty_level from exercise where concept_id = {concept_id};'
    try:
        result = conn.get_db_cursor(query)
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No exercises found for the given concept_id"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @main.route('/submit-answers', methods=['POST'])
def submit_answers(data):
    """
    Validates the user's answer against the canonical solution, records the attempt, and updates the user's mastery score for the concept.
    Expects a JSON payload with user_id, exercise_id, student_answer, and optionally hints
    """
    # data = request.json
    
    user_id = data.get("user_id")
    exercise_id = data.get("exercise_id")
    student_answer = data.get("student_answer")
    hints_used = data.get("hints_used", 0)

    concept_id_query = f"SELECT concept_id FROM exercise WHERE exercise_id = {exercise_id};"
    try:
        concept_id = conn.get_db_cursor(concept_id_query)[0]['concept_id']
    except Exception as e:
        return jsonify({"error": "Invalid exercise_id or error fetching concept_id: " + str(e)}), 400

    query = f"SELECT canonical_solution FROM exercise WHERE exercise_id = {exercise_id};"
    try:
        result = conn.get_db_cursor(query)
        canonical_solution = result[0]['canonical_solution'].strip().split()[-1]
        is_correct = (student_answer.strip() == canonical_solution)

        query = f"INSERT INTO attempts (user_id, exercise_id, student_answer, is_correct, hints_used) VALUES ({user_id}, {exercise_id}, '{student_answer}', {is_correct}, {hints_used});"
        try:
            conn.push_db_cursor(query)
        except Exception as e:
            print("Error inserting attempt data:", str(e))

        if not result:
            return jsonify({"error": "Exercise not found"}), 404
        
        update_mastery(user_id, concept_id)
        return jsonify({
            "is_correct": is_correct,
            "canonical_solution": canonical_solution,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @main.route('/ai-query', methods=['POST'])    
# This route is used for testing the AI query function. It receives a user query, checks the cache for a response, and if not found, calls the AI engine to generate a response. The response is then cached for future queries.
def ai_query(data):
    """
    Receives a user query, checks the cache for a response, and if not found, calls the AI engine to generate a response. The response is then cached for future queries.
    Expects a JSON payload with a "query" field containing the user's question or problem statement
    """
    # Get data from Post request
    # data = request.json

    query = data.get("query", "")
    
    if not query:
        return {"error": "Query is required"}
    
    # Checking Cache
    cache_response = conn.get_db_cursor("SELECT ai_response from ai_cache where user_query = %s;", (query,))
    if cache_response:
        return {
            "source": "cache",
            "data" : cache_response[0]["ai_response"]
        }
    
    # If not found in cache Calling AI ENgine
    ai_json = aiEngine.gen_ai_response(query)
    ai_response = {
        "source": "ai",
        "data": ai_json
    }

    # Caching AI response
    try:
        safe_json = json.dumps(ai_json, ensure_ascii=False)
        conn.push_db_cursor("""
        INSERT INTO ai_cache (user_query, ai_response)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE ai_response = VALUES(ai_response)
        """, (query, safe_json))
    except Exception as e:
        print("Error caching AI response:", str(e))

    return ai_response

@main.route("/query-router", methods=["POST"])
def query_router():
    user_query = request.json
    resolved_solution = ai_query(user_query)
    return jsonify({"resolved_solution": resolved_solution})


# TODO: Add function to insert data generated by AI into the database for future reference and learning. This can include new exercises, hints, or even user feedback to improve the AI's responses over time.

# TODO: Add error handling and logging for database operations and AI interactions to ensure robustness and easier debugging.

# TODO: Implement user authentication and session management to personalize the learning experience and track individual progress more effectively.

# TODO: Create an admin interface to manage concepts, exercises, and monitor user progress and AI performance.

# TODO: Ceate an query validateion function to ensure that user queries are well-formed and do not contain malicious content before processing them with the AI engine.