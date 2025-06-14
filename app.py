"""app.py"""
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, fetch_by_ingredient, fetch_by_title, fetch_by_id, random, default, get_ingredients, get_instructions

# pip install - requirements.txt
# pip freeze > requirements.txt
app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db():
    """setup access to db"""
    db = sqlite3.connect('recipefinder.db')
    db.row_factory = sqlite3.Row
    return db


# def init_db():
#     """initialize db connection"""
#     with get_db() as db:
#         db.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 hash TEXT NOT NULL
#             )
#         ''')
#         db.execute('''
#                    CREATE TABLE IF NOT EXISTS saved_recipes (
#                    id integer primary key autoincrement,
#                    user_id integer not null,
#                    meal_id integer not null,
#                    foreign key (user_id) references users (id),
#                    unique (user_id, meal_id))
#                    ''')
#         db.commit()
# init_db()


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


@app.route('/save_recipe', methods=["POST"])
@login_required
def save_recipe():
    """save a recipe from the card page to a users profile"""
    if request.method == "POST":
        user = session['userid']
        meal = request.form.get('meal_id')
        try:
            with get_db() as db:
                db.execute("INSERT into saved_recipes (user_id, meal_id) Values (?, ?)", (user, meal))
                db.commit()
                flash("Recipe Saved!")
        except sqlite3.DatabaseError as e:
            print(f'Error saving recipe: {e}')
            flash("Error saving recipe")

    return redirect('/card')



@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    """User dashboard with saved recipes"""
    user = session['userid']

    try:
        with get_db() as db:
            meals = db.execute("SELECT meal_id FROM saved_recipes WHERE user_id = ?", (user,)).fetchall()
            user = db.execute("SELECT username FROM users WHERE id = ?", (user,)).fetchone()
            username = user['username'] if user else 'User'
            meal_list = []
            for meal in meals:
                meal_list.append(fetch_by_id(meal['meal_id']))
        return render_template('dashboard.html', meal_list=meal_list, username=username)
    except sqlite3.DatabaseError as e:
        print(f"Error loading dash: {e}")
        flash("Error Loading Your Recipe Cards")
        return redirect('/')





@app.route('/login', methods=["GET", "POST"])
def login():
    """log a user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get('username') or not request.form.get("password"):
            flash("Missing username or password")
            return render_template("login.html")

        try:
            with get_db() as db:
                user = db.execute(
                    "SELECT * from users where username = ?", (request.form.get("username"),)).fetchone()

                if not user or not check_password_hash(user["hash"], request.form.get("password")):
                    flash("Something went wrong, try again.")
                    return render_template("login.html")

                session['userid'] = user["id"]
                return redirect('/')
        except sqlite3.DatabaseError as e:
            print(f'Login error: {e}')
            flash("Login failed")
            return render_template('login.html')

    return render_template("login.html")


@app.route('/logout')
def logout():
    """log user out"""
    session.clear()
    return redirect('/')


@app.route("/register", methods=["GET", "POST"])
def register():
    """register a new user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            flash("Must input username and password")
            return render_template("register.html")

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        try:
            with get_db() as db:
                existing_user = db.execute(
                    "SELECT id from users where username = ?", (username,)).fetchone()
                if existing_user:
                    flash("User already exists.")
                    return render_template("register.html")


                user = db.execute(
                    "INSERT into users (username, hash) VALUES (?, ?)", (username, password))
                db.commit()
                userid = user.lastrowid

                session['userid'] = userid
                return redirect('/')

        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            flash("Registration failed. Username might already exist.")
            return render_template("register.html")


    return render_template("register.html")
