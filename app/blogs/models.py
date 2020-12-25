from app import *
from app import mongo
from bson.json_util import ObjectId


class Article():


    def add_article(self, blog):
        resp = mongo.db.articles.insert_one(blog)

        return resp


    def getAllArticles(self):
        articles = mongo.db.articles.find()

        return articles

    def deleteAnArticle(self, id):
        resp = mongo.db.articles.delete_one({'_id':ObjectId(id)})

        return resp

    def getAnArticle(self, id):
        resp = mongo.db.articles.find_one({'_id': ObjectId(id)})

        return resp

    def addLikes(self, username, likes):
        resp = mongo.db.articles.update_one({'author': username},{'$set':{'likes':likes}})

        return resp