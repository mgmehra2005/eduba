from flask import Blueprint, render_template, jsonify
from app import app
from app.db_connect import DBConnection

main = Blueprint("main", __name__)
conn = DBConnection(app.config)


@main.route("/")
def index():
    return render_template("index.html")

@app.route("/problem", methods=['GET', 'POST']) 
def problem():
    return jsonify(conn.get_db_cursor("select * from concepts;"))