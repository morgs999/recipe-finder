"""app.py"""
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from helpers import fetch, login_required
from sqlite4 import SQLite4

# pip install - requirements.txt
# pip freeze > requirements.txt
app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQLite4("recipefinder.db")
db.connect()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=["GET", "POST"])
def index():
    """home page"""
    default_recipe = fetch("Arrabiata")
    return render_template("index.html", recipe=default_recipe)


# @app.route('/recipes')
# def get_recipes():
#     """Get all recipes from database"""
#     with get_db() as db:
#         recipes = db.execute('SELECT * FROM recipes').fetchall()
#     return jsonify([dict(recipe) for recipe in recipes])
