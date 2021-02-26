from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
from flask import g
import os
from bson.json_util import ObjectId

from app import *
from app import app, mongo
from .models import Article
# app.config['IMAGE_UPLOADS'] = '/mnt/d/digital-magazine/app/static'

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
        # image = request.files['image']
        # path = os.path.join(app.config['IMAGE_UPLOADS'], image.filename)
        # image.save(path)
        dt = datetime.now()
        date = dt.strftime("%d-%m-%Y")
        time = dt.strftime("%H:%M")
        newblog = {}
        newblog['title'] = req.get('title')
        # newblog['image'] = image.filename
        newblog['domain'] = req.get('domain')
        newblog['body'] = req.get('body')
        newblog['datetime'] = {"date":date,"time":time}
        newblog['likes'] = "0"
        newblog['author'] = session['USERNAME']

        resp = article.addArticle(newblog)
        # blog_count = blog_count + 1

        return redirect(url_for('profile.index'))

    
    return render_template('create.html')


@blog.route("/<id>/delete", methods=['DELETE', 'GET'])
def delete(id):
    blog = article.deleteAnArticle(id)

    return redirect(url_for('profile.index'))

@blog.route("/<id>")
def viewfull(id):
    blog = article.getAnArticle(id)
    blogs = article.getAllArticles()
    comments = article.getAllComments()

    return render_template('view.html', blog=blog, blogs=blogs, comments=comments)


@blog.route('/<id>/comment', methods=['POST', 'GET'])
def add_comment(id):
    print("Hello")
    if request.method == 'POST':

        blog = article.getAnArticle(id)
        comment = request.form['comments']
        dt = datetime.now()
        date = dt.strftime("%d-%m-%Y")
        time = dt.strftime("%H:%M")

        author = session['USERNAME']
        new_comment = {}
        new_comment['author'] = author
        new_comment['blog_id'] = id
        new_comment['comment'] = comment
        new_comment['created'] = {'date': date, 'time': time}
        resp = article.add_comment(new_comment)

        comments = article.getAllComments()

        return redirect (url_for('blog.viewfull', id=id))

@blog.route('/<id>/update', methods=['POST', 'GET'])
def update(id):
    if request.method == 'GET':
        blog = article.getAnArticle(id)

        return render_template('update.html', article=blog)

    if request.method == 'POST':
        title = request.form['title']
        domain = request.form['domain']
        body = request.form['body']

        updated_blog = {}
        updated_blog['title'] = title
        updated_blog['domain'] = domain
        updated_blog['body'] = body

        resp = article.updateAnArticle(id, updated_blog)

        return redirect(url_for('blog.index'))


@blog.route('/myblogs', methods=['POST', 'GET'])
def my_blogs():
    username = session['USERNAME']
    email = session['EMAIL']

    articles = article.getUserArticles(username, email)

    print("articles => ", articles)

    return render_template('my_blogs.html', articles=articles)