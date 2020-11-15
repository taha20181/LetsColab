from flask import Flask
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt
import os

# Custom imports
models = Flask(__name__)
models.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(models)

class Users:

    def add_newuser(self,newuser):

        user = {
            "username": newuser['username'],
            "email": newuser['email'],
            "password": newuser['password']
        }

        mongo.db.users.insert_one(user) 
        # mongo.db.user.insert_one(user)
        # return jsonify(user),200
    
    def find_user(self,email,password):
        
        found = mongo.db.users.find_one({"email":email},{"_id":0})
        print("I FOUND SOMETHING : ",found)
        # print(found["username"])
        # return "User Found"
        
        if found is not None:
            if bcrypt.checkpw(password.encode('utf-8'), found["password"]):
                print("FOUND : ",found["username"])
                return found["username"]
            else:
                return -1
        else:
            return 0