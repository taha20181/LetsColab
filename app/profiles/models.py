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
            # "gender": newuser['gender'],
            "username": newuser['username'],
            "password": newuser['password'],
            "account created": newuser['acc_created'],
            "blog count": newuser['blog count']
        }

        mongo.db.users.insert_one(user) 

    def add_personal_info(self,info):
        user_info = {
            'first name' : info['first name'],
            'last name' : info['last name'],
            'occupation' : info['occupation'],
            'company' : info['company'],
            "github" : info['github'],
            "linkedin" : info['linkedin'],
            'country' : info['country'],
            'skills' : info['skills'],
            'about_me' : info['about_me']
        }
        print(session['EMAIL'])
        mongo.db.users.update_one({'email':session['EMAIL']},{'$set':user_info})

    def find_user(self,email,password):
        
        found = mongo.db.users.find_one({"email":email},{"_id":0})
      
        if found is not None:
            if bcrypt.checkpw(password.encode('utf-8'), found["password"]):
                # print("FOUND : ",found["username"])
                return found["username"]
            else:
                return -1
        else:
            return 0

    def get_user(self,email):
        user = mongo.db.users.find_one({'email': email})

        return user

class Data : 
    def get_skills(self):
        skills = mongo.db.skills.find({'_id':0})
        print(skills)

        return skills
    
    def add_skills(self,new_skill):
        # mongo.db.users.insert_one({})
        # mongo.db.skills.update({},{'$push':{'skills':new_skill}},upsert=True)
        a = list(mongo.db.skills.find( {},{ 'skills': { '$elemMatch': new_skill } } ))
        print("A : ",a)