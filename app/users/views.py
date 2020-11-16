from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response
from flask import session, url_for
from datetime import datetime

user = Blueprint("user", __name__, template_folder='templates', static_folder='static')

# Custom imports
from app import *
from .models import *
users = Users()

@user.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return (resp, 200)

@user.route("/")
def index():
    print(app.config)
    if session:
        print(session)
    return render_template("index.html")

@user.route("/sign-up", methods=["POST","GET"])
def sign_up():

    if request.method == "POST":
        req = request.form
        # req = request.json
        
        missing = list()
        for k, v in req.items():
            if v == "" or v == " ":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("sign_up.html", feedback=feedback)
        
        newuser={}
        newuser["username"] = req.get("username")
        newuser["email"] = req.get("email")
        password = req.get("password")
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        newuser["password"] = hashed

        users.add_newuser(newuser)
        return redirect(url_for("user.login"))
    
    return render_template("sign_up.html")

@user.route("/login", methods=["POST","GET"])
def login():

    if request.method == "POST":
        req = request.form
        
        missing = list()
        for k, v in req.items():
            if v == "" or v == " ":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("login.html", feedback=feedback)
        
        email = req.get("email")
        password = req.get("password")

        status = users.find_user(email,password)
        if type(status) == str:
            print(status)
            # session.clear()
            session['logged_in']=True
            session["USERNAME"] = status
            return render_template("index.html")
        elif status == -1:
            return "Incorrect Password"
        else:
            return "User does not exist"
    
    return render_template("login.html")


@user.route("/logout")
def logout():

    print(session)
    session['logged_in']=False
    session.pop("USERNAME", None)
    # session.clear()

    return redirect(url_for("user.login"))