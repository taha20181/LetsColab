from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
import bcrypt

profile = Blueprint("profile", __name__, template_folder='templates', static_folder='static')

# Custom imports
from app import *
from .models import *
from ..blogs.models import Article
users = Users()
article = Article()

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

@profile.route("/signup", methods=["POST","GET"])
def signup():

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
        newuser['first_name'] = req.get('fname')
        newuser['last_name'] = req.get('lname')
        newuser["gender"] = req.get('gender')
        newuser["email"] = req.get("email")
        newuser["mobile"] = req.get('mobile')
        newuser["username"] = req.get("username")
        newuser["course"] = req.get("course")
        newuser["year"] = req.get("year")
        newuser["branch"] = req.get("branch")
        newuser["spec"] = req.get("spec")
        password = req.get("password")
        confirm_passw = req.get('cpassw')
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        # confirm_hashed = bcrypt.hashpw(confirm_passw.encode('utf-8'), bcrypt.gensalt(14))
        newuser["password"] = hashed
        # newuser["confirm_password"] = confirm_hashed
        newuser['acc_created'] = datetime.now()

        if bcrypt.checkpw(confirm_passw.encode('utf-8'), hashed):
            users.add_newuser(newuser)
            return redirect(url_for("profile.login"))
        else:
            flash('Password & Confirm password do not match.')
            return redirect(url_for('profile.signup'))
               
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
            return redirect(url_for("profile.user_home"))
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

@profile.route("/home")
def user_home():
    user = session["USERNAME"]
    articles = article.getAllArticles()
    return render_template("user_home.html", articles = articles)


@profile.route('/userprofile')
def user_profile():
    username = session['USERNAME']
    user = users.get_user(username)
    temp = user['account created']
    user['account created'] = datetime.date(temp)
    return render_template('profile.html', user=user)