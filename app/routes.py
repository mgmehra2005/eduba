from flask import Blueprint, render_template, jsonify, request
from app import app
from app.db_connect import DBConnection
from app.eduba_engine import update_mastery

main = Blueprint("main", __name__)
conn = DBConnection(app.config)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/concepts", methods=['GET']) 
def concepts():
    return jsonify(conn.get_db_cursor("select * from concepts;"))

@main.route('/exercises/<int:concept_id>', methods=['GET'])
def exercise(concept_id):
    query = f'select exercise_id, problem_text, difficulty_level from exercise where concept_id = {concept_id};'
    try:
        result = conn.get_db_cursor(query)
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No exercises found for the given concept_id"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/submit-answers', methods=['POST'])
def submit_answers():
    data = request.json
    
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

