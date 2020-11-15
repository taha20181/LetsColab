from flask import Flask
# from flask_pymongo import PyMongo

app = Flask(__name__)


from .users.views import user
from .blogs.views import blog

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(blog, url_prefix='/blog')