from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE,BCRPYT 
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls,form):
        hashed_pw = BCRPYT.generate_password_hash(form['password'])
        data = {
            **form,
            "password" : hashed_pw
        }
        query = """INSERT INTO users (first_name,last_name,email,password)
                VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_user_by_email(cls, email):
        data = {
            'email' : email
        }
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def get_user_by_id(cls, id):
        data = {
            'id' : id
        }
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def validate_login(cls,form):
        is_valid = True
        found_user = cls.get_user_by_email(form['email'])
        if not cls.get_user_by_email(form['email']):
            flash('Invalid Login!')
            return False
        else: 
            if not BCRPYT.check_password_hash(found_user.password, form['password']):
                flash("Invalid Login!")
                return False
        return found_user

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name is too short!")
            is_valid = False

        if len(data['last_name']) < 2:
            flash("Last name is too short!")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password is too short!")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Email must be vaild!")
            is_valid = False

        if User.get_user_by_email(data['email']):
            flash("Email already in use!")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Your passwords don't match!")
            is_valid = False

        return is_valid


