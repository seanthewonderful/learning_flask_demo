from src import app
from flask import render_template
from datetime import datetime
from src.template_filters import clean_date


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
    date = datetime.utcnow()
    my_html = "<h1>This is my html string</h1>"
    suspicious = "<script>alert('YOU GOT HACKED')</script>"
    return render_template("public/jinja.html",
                           friends=friends,
                           name=name,
                           date=date,
                           clean_date=clean_date,
                           my_html=my_html,
                           suspicious=suspicious)