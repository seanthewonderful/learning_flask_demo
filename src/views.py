from src import app
from flask import (render_template, redirect, request, 
                   jsonify, make_response, send_from_directory, abort,
                   make_response, session, url_for, flash)
from datetime import datetime
from src.template_filters import clean_date
import os
from werkzeug.utils import secure_filename


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


def allowed_image(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]
    
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
    
def allowed_image_filesize(filesize):
    if int(filesize) > app.config["MAX_IMG_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    
    if request.method == "POST":
        
        if request.files:
            
            if allowed_image_filesize(request.cookies.get("filesize")):
                print("File exceeded maximum size")
                return redirect(request.url)
            
            image = request.files["image"]
            # print(request.cookies)
            
            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension isn't allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            
            print("image saved")
            
            return redirect(request.url)
    
    return render_template("public/upload_image.html")


@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)
        

@app.route("/get-csv/<filename>")
def get_csv(filename):
    try:
        return send_from_directory(app.config["CLIENT_CSV"], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
        
        
@app.route("/get-report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(app.config["CLIENT_REPORT"], path=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/cookies")
def cookies():
    
    res = make_response("Cookies", 200)
    
    cookies = request.cookies
    
    flavor = cookies.get("flavor")
    sugar_type = cookies.get("sugar type")
    chewy = cookies.get("chewy")
    
    print(flavor, sugar_type, chewy)
    
    res.set_cookie(
        key="flavor", 
        value="chocorate chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=True,
        httponly=False
        )
    res.set_cookie(
        "sugar type", 
        "brown"
    )
    res.set_cookie("chewy", "yes")
    
    return res


users = {
    "sean": {
        "username": "sean",
        "email": "s@s.com",
        "password": "asdf",
        "bio": "Famous man who likes the finer things"
    },
    "natalie": {
        "username": "natalie",
        "email": "n@n.com",
        "password": "asdf",
        "bio": "Infamous female who likes the worser things"
    }
}

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    
    if request.method == "POST":
        
        req = request.form
        username = req.get("username")
        password = req.get("password")
        
        if not username in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]
            
        if not password == user["password"]:
            print("password incorrect")
            return redirect(request.url)
        else:
            # Create a session key. Sessions are kinda like dictionaries
            # This is insecure... duh
            session["USERNAME"] = user["username"]
            session["PASSWORD"] = user["password"]
            print("user added to session")
            return redirect(url_for("profile"))
    
    return render_template("public/sign_in.html")


@app.route("/profile")
def profile():
    
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = users[username]
        
        return render_template("public/profile.html", user=user)
    else:
        print("username not found in session")
        return redirect(url_for('sign-in'))
    

@app.route("/sign-out")
def sign_out():
    
    session.pop("USERNAME", None)
    
    return redirect(url_for("sign-in"))


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    
    if request.method == "POST":
        
        req = request.form
        
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        
        if not len(password) >= 19:
            flash("Password must be at least 10 characters in length", category="danger")
            return redirect(request.url)
        
        flash("account created", category="success")
        return redirect(request.url)
    
    return render_template("public/sign-up.html")


""" HTTP Route stuff """

stock = {
    "fruit": {
        "apple": 30,
        "banana": 45,
        "cherry": 1000
    }
}

@app.route("/get-text")
def get_text():
    return "Some Text"


@app.route("/index2")
def index2():  
    return render_template("public/index2.html")

@app.route("/qs")
def qs():
    
    if request.args:
        res = request.args
        return " ".join(f"{k}: {v}" for k, v in res.items())
    
    return "No query"


@app.route("/stock")
def get_stock():
    
    res = make_response(jsonify(stock), 200)
    
    return res


@app.route("/stock/<collection>")
def get_collection(collection):
    
    """ Returns the collection from stock """
    
    if collection in stock:
        res = make_response(jsonify(stock[collection]), 200)
        return res
    
    res = res = make_response(jsonify({"error":"Item not found"}), 400)
    return res


@app.route("/stock/<collection>", methods=["POST"])
def create_collection(collection):
    
    """ Creates new colection if it doesn't exist """
    
    req = request.get_json()
    
    if collection in stock:
        res = make_response(jsonify({"error":"Collection already exists"}), 400)
        return res
    
    stock.update({collection: req})
    
    res = make_response(jsonify({"message":"Collection created"}), 200)
    return res


@app.route("/stock/<collection>/<item>")
def get_item(collection, item):
    
    """ Returns the qty of the item """
    
    if collection in stock:
        item = stock[collection].get(item)
        if item:
            res = make_response(jsonify(item), 200)
            return res
        
        res = make_response(jsonify({"error":"Unknown item"}), 400)
        return res
    
    res = res = make_response(jsonify({"error":"Collection not found"}), 400)
    return res

# GET & POST
@app.route("/add-collection", methods=["GET", "POST"])
def add_collection():
    """
    Renders a template if request method is GET.
    Creates a collection if request method is POST or if collection doesn't exist
    """

    if request.method == "POST":
        
        req = request.form
        collection = req.get("collection")
        item = req.get("item")
        qty = req.get("qty")
        
        if collection in stock:
            message = "Collection already exists"
            return render_template("public/add_collection.html", stock=stock, message=message)
        
        stock[collection] = {item: qty}
        message = "Collection created"
        
        return render_template("public/dd_collection.html", stock=stock, message=message)
    
    return render_template("public/add_collection.html", stock=stock)


# PUT a collection
@app.route("/stock/<collection>", methods=["PUT"])
def put_colection(collection):
    
    """ Replaces (overwrites all previous) or creates a collection. Expected body: {"member": qty} """
    
    req = request.get_json()
    
    stock[collection] = req
    
    res = make_response(jsonify({"message":"Collection replaced!"}), 200)
    return res


# PATCH a collection
@app.route("/stock/<collection>", methods=["PATCH"])
def patch_collection(collection):
    
    """ Updates or creates a collection. Expected body: {"member": qty} """
    
    req = request.get_json()
    
    if collection in stock:
        for k, v in req.items():
            stock[collection][k] = v
            
        res = make_response(jsonify({"message":"Collection updates"}), 200)
        return res
    
    stock[collection] = req
    
    res = make_response(jsonify({"message": "Collection creates"}), 200)
    return res

# DELETE a collection
@app.route("/stock/<collection>", methods=["DELETE"])
def delete_collection(collection):
    
    """ If collection exists, delete it """
    
    if collection in stock:
        del stock[collection]
        res = make_response(jsonify({}), 204) # Create emptiness to return, code 204 signifies it
        return res
    
    res = make_response(jsonify({"error": "collection not found"}), 400)
    return res

# DELETE an item
@app.route("/stock/<collection>/<item>", methods=["DELETE"])
def delete_item(collection, item):
    
    """ If collection and item exist, delete item """
    
    if collection in stock:
        if item in stock[collection]:
            del stock[collection][item]
            res = make_response(jsonify({}), 204) # Create emptiness to return, code 204 signifies it
            return res
        
        res = make_response(jsonify({"error": "item not found"}), 400)
        return res 
    
    res = make_response(jsonify({"error": "collection not found"}), 400)
    return res


""" Task queues with Flask and Redis """

import redis
from rq import Queue
import time

r = redis.Redis()
q = Queue(connection=r)

# I installed Redis without homebrew, now it is working fine. 
# CLI command: redis-server = starts Redis terminal. commands below in different terminal
# CLI command: rq worker = starts Redis listening terminal for this command
# ^^ rq is a Redis thing, not referring to variables.

def background_task(n):
    
    delay = 2
    
    print("Task running")
    print(f"Simulating {delay} second delay")
    
    time.sleep(delay)
    
    print(len(n))
    print("Task complete")
    
    return len(n)


@app.route("/task")
def add_task():
    
    if request.args.get("n"):
        
        job = q.enqueue(background_task, request.args.get("n"))
        
        q_len = len(q)
        
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue."
    
    return "No value for n"

