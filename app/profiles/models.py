from flask import Flask, session
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt

# Custom imports
from app import *
from app import mongo

class Users:

    def add_newuser(self,newuser):

        user = {
            "first name": newuser['first_name'],
            "last name": newuser['last_name'],
            "email": newuser['email'],
            "gender": newuser['gender'],
            "mobile": newuser['mobile'],
            "username": newuser['username'],
            "course": newuser['course'],
            "year": newuser['year'],
            "branch": newuser['branch'],
            "spec": newuser['spec'],
            "password": newuser['password'],
            # "confirm password": newuser['confirm_password'],
            "account created": newuser['acc_created']
        }

        mongo.db.users.insert_one(user) 

    def add_personal_info(self,info):
        user_info = {
            'username' : info['username'],
            'first name' : info['first name'],
            'last name' : info['last name'],
            'address' : info['address'],
            'city' : info['city'],
            'country' : info['country'],
            'postal_code' : info['postal_code'],
            'about_me' : info['about_me']
        }
        print(session['EMAIL'])
        mongo.db.users.update_one({'email':session['EMAIL']},{'$set':user_info})

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