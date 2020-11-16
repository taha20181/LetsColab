from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config.Config")
mongo = PyMongo(app)

from .profiles.views import profile
from .blogs.views import blog

app.register_blueprint(profile, url_prefix='/')
app.register_blueprint(blog, url_prefix='/blog')