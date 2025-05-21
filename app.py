from flask import Flask, render_template, request

app = Flask(__name__)


#här la jag in recepten istället för hela databasen. Det blev för mycket och dessutom var den på engelska.
recept = [
    {
        "titel": "Pannkakor",
        "ingredienser": ["mjöl", "ägg", "mjölk", "smör", "salt"]
    },
    {
        "titel": "Köttfärssås",
        "ingredienser": ["pasta", "köttfärs", "lök", "krossade tomater"]
    },
    {
        "titel": "Potatissallad",
        "ingredienser": ["potatis", "gräddfil", "majonnäs", "purjolök", "salt", "peppar"]
    },
    {
        "titel": "Korv Stroganoff",
        "ingredienser": ["falukorv", "lök", "tomatpure", "grädde"]
    },
    {
        "titel": "Pasta Alfredo",
        "ingredienser": ["pasta", "grädde", "parmesanost"]
    }
]


@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    user_ingredients = []
    if request.method == "POST":
        ingredients_input = request.form.get("ingredients", "")
        if ingredients_input:
            user_ingredients = [i.strip().lower() for i in ingredients_input.split(",") if i.strip()]
            for r in recept:
                har = [ing for ing in r["ingredienser"] if ing in user_ingredients]
                saknas = [ing for ing in r["ingredienser"] if ing not in user_ingredients]
                if har:
                    matches.append({
                        "titel": r["titel"],
                        "har": har,
                        "saknas": saknas
                    })
            matches = sorted(matches, key=lambda m: len(m["har"]), reverse=True)
    return render_template("index.html", matches=matches, user_ingredients=", ".join(user_ingredients))

if __name__ == "__main__":
    app.run(debug=True)
