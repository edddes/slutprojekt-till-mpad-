from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_recipes():
    # Hämtar alla recept från databasen
    conn = sqlite3.connect("5k-recipes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Title, Ingredients FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def match_recipes(user_ingredients, recipes):
    matches = []
    for title, ingredients in recipes:
        # Gör om ingredienssträngen till en lista och små bokstäver
        recipe_ings = [ing.strip().lower() for ing in ingredients.split(',')]
        matched = [ing for ing in recipe_ings if ing in user_ingredients]
        missing = [ing for ing in recipe_ings if ing not in user_ingredients]
        if matched:
            matches.append({
                "name": title,
                "matched": matched,
                "missing": missing
            })
    return matches

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    user_ingredients = []
    if request.method == "POST":
        ingredients_input = request.form.get("ingredients", "")
        if ingredients_input:
            user_ingredients = [i.strip().lower() for i in ingredients_input.split(",") if i.strip()]
            recipes = get_recipes()
            matches = match_recipes(user_ingredients, recipes)
            # Visa max 10 förslag, sorterat på flest matchade ingredienser
            matches = sorted(matches, key=lambda m: len(m["matched"]), reverse=True)[:10]
    return render_template("index.html", matches=matches, user_ingredients=", ".join(user_ingredients))

if __name__ == "__main__":
    app.run(debug=True)
