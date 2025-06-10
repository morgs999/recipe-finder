"""helper functions"""
from functools import wraps
import requests
from flask import redirect, session


def login_required(f):
    """decorator for logging in auth"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userid") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def default():
    """Fetch Arrabiata as default recipe"""
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recipe = data.get("meals", [])
    return recipe[0] if recipe else None


def fetch_by_title(search):
    """Fetch by Meals Title"""
    url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={search}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recipe = data.get('meals', [])
    return recipe[0] if recipe else None


def fetch_by_ingredient(search):
    """Fetch a Recipe by Ingredient Lookup"""
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        recipe = data.get("meals", [])
        return recipe[0] if recipe else None
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def fetch_by_id(id):
    """fetch a recipe by meal ID"""
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recipe = data.get("meals", [])
    return recipe[0] if recipe else None


def random():
    """fetch a random recipe"""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recipe = data.get("meals", [])
    return recipe[0] if recipe else None


def get_ingredients(recipe):
    """separate ingredients and measurements"""
    ingredients = []
    for i in range(1,21):
        ingredient = recipe.get(f'strIngredient{i}')
        measure = recipe.get(f'strMeasure{i}')

        if ingredient and ingredient.strip():
            ingredients.append({
                'ingredient': ingredient,
                'measure': measure
            })
    return ingredients


def get_instructions(recipe):
    """separate individual cooking instructions"""
    text = recipe["strInstructions"]
    lines = text.split(". ")
    # print(lines[0])
    return lines
