from src import app
from flask import render_template


@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/jinja")
def jinja():
    friends = ["Kellen", "Drew", "Clark", "Sparks", "Cody"]
    name = "sean"
    return render_template("public/jinja.html",
                           friends=friends,
                           name=name)