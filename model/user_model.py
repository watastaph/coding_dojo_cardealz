from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod 
    def validate_user(user):
        is_valid=True
        if len(user['txtFname']) < 2:
            flash("first name must be at 2 characters")
            is_valid=False
        if len(user['txtLname']) < 2:
            flash("last name must be at 2 characters")
            is_valid=False
        if len(user['txtPword']) < 8:
                flash("Password must be at 8 characters")
                is_valid=False
        if not EMAIL_REGEX.match(user['txtEmail']):
            flash("Invalid Email Address!")
            is_valid = False
        if user['txtPword'] != user['txtConfirmPword'] :
            flash("Password not match!")
            is_valid=False
        return is_valid

    @staticmethod 
    def validate_user(user):
        is_valid=True
        if len(user['txtFname']) < 2:
            flash("first name must be at 2 characters")
            is_valid=False
        if len(user['txtLname']) < 2:
            flash("last name must be at 2 characters")
            is_valid=False
        if len(user['txtPword']) < 8:
            flash("Password must be at 8 characters")
            is_valid=False
        if not EMAIL_REGEX.match(user['txtEmail']):
            flash("Invalid Email Address!")
            is_valid = False
        if user['txtPword'] != user['txtConfirmPword'] :
            flash("Password not match!")
            is_valid=False
        return is_valid
	
    @staticmethod 
    def validate_login(user):
        is_valid=True
        if len(user['txtPword']) < 8:
            flash("Password must be at 8 characters")
            is_valid=False
        if not EMAIL_REGEX.match(user['txtEmail']):
            flash("Invalid Email Address!")
            is_valid = False
        return is_valid

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (firstname , lastname, email, password, created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(email)s , %(pword)s, NOW(), NOW() );"
        return connectToMySQL('db').query_db( query, data )
    
    @classmethod
    def verify_user(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL('db').query_db( query, data )
        if len(results) < 1:
            return False
        return cls(results[0])