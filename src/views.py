from src import app
from flask import render_template, request, jsonify, make_response
from datetime import datetime
from src.template_filters import clean_date


@app.route("/")
def index():
    print(f"FLASK_ENV set to: {app.config['ENV']}")
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
    
@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        
        req = request.get_json()
        
        response = {
            "message": "JSON received!",
            "name": req.get("name")
        }
        
        res = make_response(jsonify(response), 200)
        
        return res
    else:
        n_response = {
            "message": "No JSON received"
        }
        res = make_response(jsonify(n_response), 400)
        return res
    
@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    
    req = request.get_json()
    
    print(req)
    
    res = make_response(jsonify(req), 200)
    
    return res

@app.route("/query")
def query():
    # query_string = "?foo=foo&bar=bar&baz=baz&title=query+strings+with+flask"
    
    if request.args:
        args = request.args
        # for k, v in args.items():
        #     print(f"{k}: {v}")
        
        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())
        
        return f"(Query) {serialized}", 200
    else:
        
        return "No query received", 200
    


