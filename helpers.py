"""helper functions"""
from functools import wraps
import requests
from flask import redirect, session


def login_required(f):
    """decorator for logging in auth"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
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


def fetch(search):
    """Fetch a Recipe"""
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


def random():
    """fetch a random recipe"""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recipe = data.get("meals", [])
    return recipe[0] if recipe else None


def ingredients():
    """separate ingredients and measurements"""
    return True


def instructions():
    """separate individual cooking instructions"""
    return True
