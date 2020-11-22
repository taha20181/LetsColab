from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
from flask import g

from app import *
from .models import Article

blog = Blueprint("blog", __name__, template_folder='templates', static_folder='static')

article = Article()

@blog.route("/")
def index():
    return "View All Blogs here"


@blog.route('/create', methods=['POST', 'GET'])
def create():
    ###########################
    # Check for login code here
    ###########################
    if request.method == 'POST':
        req = request.form

        newblog = {}
        newblog['title'] = req.get('title')
        newblog['image'] = req.get('image')
        newblog['domain'] = req.get('domain')
        newblog['body'] = req.get('body')
        newblog['datetime'] = datetime.now()
        newblog['author'] = session['USERNAME']

        print(newblog)

        resp = article.add_article(newblog)

        return redirect(url_for('profile.user_home'))

    
    return render_template('create.html')