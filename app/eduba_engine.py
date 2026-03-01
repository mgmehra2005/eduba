from flask import jsonify, json
from app import app
from app.db_connect import DBConnection
import requests

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


class EdubaAIEngine:
    
    HF_API_KEY = app.config["HF_API_KEY"]
    API_URL = "https://router.huggingface.co/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
    }

    SYSTEM_PROMPT = """
    You are Eduba, an explainable academic AI assistant.

    Respond strictly in JSON format:

    {
    "concept": "topic name",
    "difficulty": "Beginner/Intermediate/Advanced",
    "stepwise_explanation": [
        "Step 1 explanation",
        "Step 2 explanation",
        "Step 3 explanation"
    ],
    "final_answer": "short final answer"
    }
    """

    @staticmethod
    def gen_ai_response(user_query):
        prompt = EdubaAIEngine.SYSTEM_PROMPT + "\nUser Question: " + user_query

        payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "meta-llama/Llama-3.2-1B-Instruct:novita"
        }
        try:
            response = requests.post(EdubaAIEngine.API_URL, headers=EdubaAIEngine.headers, json=payload)

            if response.status_code != 200:
                return {
                    "concept": "System Error",
                    "difficulty": "Beginner",
                    "stepwise_explanation": [
                        f"HF API returned status {response.status_code}"
                    ],
                    "final_answer": "Error"
                }

            result = response.json()
            text_output = result["choices"][0]["message"]["content"]

            # Extract JSON safely
            json_start = text_output.find("{")
            json_end = text_output.rfind("}") + 1

            if json_start == -1 or json_end == -1:
                raise ValueError("JSON not found in response")

            json_string = text_output[json_start:json_end]

            return json.loads(json_string)
        except Exception as e:
            return {
            "concept": "AI Error",
            "difficulty": "Beginner",
            "stepwise_explanation": [
                "AI response parsing failed.",
                str(e)
            ],
            "final_answer": "Error"
            }