# RECIPE FINDER

## My Final Project for [CS50](https://cs50.harvard.edu/x/2025/):

I built a dynamic recipe finder that utilizes the [Meal Db API](https://www.themealdb.com/api.php) to give users recipes back after searching for an ingredient.
 - Got some onion left in the fridge?  Try some Moroccan Carrot Soup!
 - Bought some beef at the supermarket? Here's a recipe for Szechuan Beef!
 - Not sure what dishes use lemon?  Try Tahini Lentils!

## Description

I utilized a lot of the code from our Finance problem set, such as the login and register functionality.  But I did have to learn to use SQLite without the CS50 training wheels which was fun.  I went down a bit of a rabbit hole trying to find a SQLite PiP library that would do the work for me, but decided to just go back to the built in SQLite functionality of Python.

Using the MealDB API was an excellent learning experience in how to fetch and parse and give data baack to the user in a meaningful way.  I ended up creating helper functions (in helpers.py) that would fetch a default or random recipe, lookup recipes by ingrdient, title, or ID, and divy up ingredients, measurements, and instructions in a pleasing way for the end user.  This really helped me get better at some nuts and bolts Python like "in range", appending to dictionaries and lists, and splitting huge blocks of text down to manageable chunks.

I did use Github Copilot (as well as SQLite's somewhat jargon-y documentation) to learn how to connect to, insert into, and query my SQLite database.  Though I did try and write each connection from scratch, I did need help in connecting to the DB, though I ended up not using all of the suggestions (such as initializing the DB every time the app starts).

The three big pieces of functionality are the search by ingredient bar, the Recipe card page, and the user dashboard.

### Search by Ingrdient
The user searches by ingredient and is returned 10 random recipe results from the Meal DB API.  This was actually done with Javascript within the index.html template.  Though I did need some Copilot help with the random result return, the rest was relatively simple:  take the input ingredient, fetch from the API filtered for the ingredient, create individual rows with the thumbnail and meal title from the fetch, and then fill in the input value to be submitted.

Though I used some of the "quote" example from the Finance problem set, creating a visual search result was the toughest thing to come up with.

### Recipe Card Page
Once the search has been complete and the "get cookin'" button clicked, the recipe card takes over.

The meal is fetched from the API by title (though there is a fetch by ingredient as well), and the get_ingredients and get_instructions functions provide more digestible from the JSON data fetched.  The template then has 3 different sets of data to provide to the user, recipe, ingrdients, and instructions.  There is also a Youtube link if the user would like to see a video of the recipe.

If there is a User logged in (and therefore a "userid" saved within the Flask session) a "Save this Recipe" button will appear above the thumbnail, allowing the user to store a link to this recipe within their user dashboard (through SQLite).

### User Dashboard
If the User is logged in (and therefore there is a "userid" saved within the Flask session), a "My Recipes" link along the navbar will allow them to see their dashboard of saved recipe cards.

These cards are generated solely by ID, meaining a SQLite table that only contains the meal_id (provided by Meal DB) and a foreign key with the users id is stored within the database.  This means that a fetch is performed for every single card the user has saved; I debated whether to lean more towards db storage or individual fetches and decided at this small scale to let the API handle the bulk of the work.  If this were a real world application, storing more data in SQLite would be more efficient for the apps runtime, but it was just a small project.

A "meal_list" is compiled by fetching each recipe the user has a saved meal id for, and then providing that list forward to the dashboard template, which generates individual cards for each meal in meal_list.


### [Video Demo](https://youtu.be/4bLbsLj8pF0)

### [GitHub Repo](https://github.com/morgs999/recipe-finder)

## Libraries Used
<img src="static/python.svg" alt="drawing" width="50"/>
Python
<img src="static/flask.svg" alt="drawing" width="50"/>
Flask
<img src="static/sqlite.svg" alt="drawing" width="50"/>
SQLite
<img src="static/html5.svg" alt="drawing" width="50"/>
HTML
<img src="static/bootstrap.svg" alt="drawing" width="50"/>
Bootstrap CSS
<img src="static/javascript.svg" alt="drawing" width="50"/>
Javascript