from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
from flask import g

from app import *
from .models import Article

blog = Blueprint("blog", __name__, template_folder='../templates/blog', static_folder='static', static_url_path='static')

article = Article()

@blog.route("/")
def index():
    art = list(article.getAllArticles())
    # print(art)
    return render_template('all_articles.html',articles=art)


@blog.route('/create', methods=['POST', 'GET'])
def create():
    ###########################
    # Check for login code here
    ###########################
    if request.method == 'POST':
        req = request.form
        dt = datetime.now()
        date = dt.strftime("%a, %d.%m.%Y")
        time = dt.strftime("%H:%M")
        newblog = {}
        newblog['title'] = req.get('title')
        newblog['image'] = req.get('image')
        newblog['domain'] = req.get('domain')
        newblog['body'] = req.get('body')
        newblog['datetime'] = {"date":date,"time":time}
        newblog['author'] = session['USERNAME']

        resp = article.add_article(newblog)

        return redirect(url_for('profile.user_home'))

    
    return render_template('create.html')


@blog.route("/<id>/delete", methods=['DELETE', 'GET'])
def delete(id):
    blog = article.deleteAnArticle(id)

    print(blog)

    return redirect(url_for('profile.index'))