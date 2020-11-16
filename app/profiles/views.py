from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session

profile = Blueprint("profile", __name__, template_folder='templates', static_folder='static')

# Custom imports
from app import *
from .models import *
users = Users()

@profile.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return (resp, 200)

@profile.route("/")
def index():
    if session:
        if session['logged_in'] == True:
            return redirect(url_for("profile.user_profile"))
    return render_template("index.html")

@profile.route("/sign-up", methods=["POST","GET"])
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
        return redirect(url_for("profile.login"))
    
    return render_template("sign_up.html")

@profile.route("/login", methods=["POST","GET"])
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
            session.clear()
            session['logged_in']=True
            session["USERNAME"] = status
            print("SESSION LOGIN : ",session)
            return redirect(url_for("profile.index"))
        elif status == -1:
            return "Incorrect Password"
        else:
            return "User does not exist"
    
    return render_template("login.html")


@profile.route("/logout")
def logout():

    print("AT LOGOUT : ",session)
    session['logged_in'] = False
    session.pop("USERNAME", None)
    print("SESSION LOGOUT : ",session)
    session.clear()
    return redirect(url_for("profile.index"))

@profile.route("/show_session")
def show_session():
    print("SHOW SESSION : ",session)
    return ""

@profile.route("/profile")
def user_profile():
    user = session["USERNAME"]
    return render_template("profile.html",user=user)