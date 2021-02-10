from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
import bcrypt
from flask import g
import os


profile = Blueprint("profile", __name__, template_folder='../templates/profile', static_folder='static',static_url_path='static')

# Custom imports
from app import *
from app import app
from .models import *
from ..blogs.models import Article
users = Users()
article = Article()
app.config['IMAGE_UPLOADS'] = "/mnt/d/Taha/digi_magazine/app/images/"

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
            articles = article.getAllArticles()
            return render_template("user_home.html", articles = articles)

    articles = article.getAllArticles()
    return render_template("user_home.html", articles = articles)
    
@profile.route("/",methods=['POST'])
def index_like():
    if session:
        if session['logged_in'] == True:
            a = 200
            author = article.addLikes(session['USERNAME'],a)
            # print("AUTHOR : ",author)
            
            req = request.get_json()
            print("REQ : ",req)
            # res = make_response(jsonify(req), 200)
            # articles = article.getAllArticles()
            return ""
    return ""
    # articles = article.getAllArticles()
    # return render_template("user_home.html", articles = articles)

@profile.route("/signup", methods=["POST","GET"])
def signup():

    if request.method == "POST":
        req = request.form
        # image = request.files['image']
        # path = os.path.join(app.config['IMAGE_UPLOADS'], image.filename)
        # image.save(path)
        
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
        # newuser['image'] = path
        # newuser["gender"] = req.get('gender')
        newuser["email"] = req.get("email")
        # newuser["mobile"] = req.get('mobile')
        newuser["username"] = req.get("username")
        newuser['blog count'] = "0"
        # newuser["course"] = req.get("course")
        # newuser["year"] = req.get("year")
        # newuser["branch"] = req.get("branch")
        # newuser["spec"] = req.get("spec")
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
            session['EMAIL'] = email
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
    session.pop("EMAIL", None)
    print("SESSION LOGOUT : ",session)
    session.clear()
    return redirect(url_for("profile.index"))

# @profile.route("/show_session")
# def show_session():
#     print("SHOW SESSION : ",session)
#     return ""

# @profile.route("/home")
# def user_home():
#     user = session["USERNAME"]
#     articles = article.getAllArticles()
#     return render_template("user_home.html", articles = articles)


@profile.route('/userprofile', methods=['GET','POST'])
def user_profile():
    if request.method=='GET':
        if session:
            email = session['EMAIL']
            user = users.get_user(email)
            return render_template('profile.html', user=user)
        return redirect(url_for("profile.index"))
    else:
        req = request.form
        print(req)
        info = {
            'first name' : req.get('first_name'),
            'last name' : req.get('last_name'),
            'occupation' : req.get('occupation'),
            'company' : req.get('company'),
            "github" : req.get('github'),
            "linkedin" : req.get('linkedin'),
            'country' : req.get('country'),
            'about_me' : req.get('about_me')
        }
        print(info)
        users.add_personal_info(info)
        return redirect(request.url)


@profile.route('/project')
def project():
    return render_template('base_templates/comingsoon.html')