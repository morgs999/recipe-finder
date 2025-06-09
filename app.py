"""app.py"""
from sqlite4 import SQLite4
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from helpers import login_required, fetch_by_ingredient, fetch_by_title, random, default, get_ingredients, get_instructions

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
    default_recipe = random()
    return render_template("index.html", recipe=default_recipe)


@app.route('/card', methods=["GET", "POST"])
# @login_required
def card():
    """recipe card page"""
    if request.method == "POST":
        if request.form.get("ingredient"):
            recipe = fetch_by_ingredient(request.form.get("ingredient"))
        else:
            recipe = fetch_by_title(request.form.get('title'))
        ingredients = get_ingredients(recipe)
        instructions = get_instructions(recipe)
        return render_template("card.html", recipe=recipe, ingredients=ingredients, instructions=instructions)

    recipe = default()
    ingredients = get_ingredients(recipe)
    instructions = get_instructions(recipe)
    return render_template("card.html", recipe=recipe, ingredients=ingredients, instructions=instructions)
