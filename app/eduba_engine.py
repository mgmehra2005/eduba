from flask import jsonify
from app import app
from app.db_connect import DBConnection

conn = DBConnection(app.config)


def update_mastery(user_id, concept_id):
    query = f"SELECT a.is_correct, a.hints_used FROM attempts a JOIN exercise e ON a.exercise_id = e.exercise_id WHERE a.user_id = {user_id} AND e.concept_id = {concept_id}"

    result = conn.get_db_cursor(query)
    if not result :
        raise Exception("Error in fetching data for mastery_score")

    total = len(result)
    correct = sum(1 for a in result if a["is_correct"])
    total_hints = sum(a["hints_used"] for a in result)


    accuracy_rate = correct/total

    max_possible_hints = total * 3
    hint_efficiency = 1 - (total_hints / max_possible_hints)

    streak = 0
    max_streak = 0

    for attempt in result:
        if attempt["is_correct"]:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    consistency_score = max_streak / total

    mastery_score = ((0.6 * accuracy_rate) + (0.3 * hint_efficiency) + (0.1 * consistency_score))

    if mastery_score < 0.5:
        level = "Beginner"
    elif mastery_score < 0.8:
        level = "Practicing"
    else:
        level = "Mastered"

    update_mastery_score_query = f"INSERT INTO mastery (user_id, concept_id, accuracy_rate, hint_efficiency, consistency_score, mastery_score, mastery_level, streak) Values ({user_id}, {concept_id}, {accuracy_rate}, {hint_efficiency}, {consistency_score}, {mastery_score}, '{level}', {streak}) ON DUPLICATE KEY UPDATE accuracy_rate = VALUES(accuracy_rate), hint_efficiency = VALUES(hint_efficiency), consistency_score = VALUES(consistency_score), mastery_score = VALUES(mastery_score), mastery_level = VALUES(mastery_level), streak = VALUES(streak);"

    conn.push_db_cursor(update_mastery_score_query)