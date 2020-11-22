from app import *
from app import mongo


class Article():


    def add_article(self, blog):
        resp = mongo.db.articles.insert_one(blog)

        return resp


    def getAllArticles(self):
        articles = mongo.db.articles.find()

        return articles