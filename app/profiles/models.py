from flask import Flask
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt

# Custom imports
from app import *

class Users:

    def add_newuser(self,newuser):

        user = {
            "first name": newuser['first_name'],
            "last name": newuser['last_name'],
            "email": newuser['email'],
            "mobile": newuser['mobile'],
            "username": newuser['username'],
            "course": newuser['course'],
            "branch": newuser['branch'],
            "password": newuser['password'],
            "confirm password": newuser['confirm_password']
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

    def get_user(self,username):
        user = mongo.db.users.find_one({'username': username})

        return user