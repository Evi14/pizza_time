from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db_name = 'pizza'
class User:
    db_name = "pizza"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,address, city, state, password) VALUES(%(first_name)s,%(last_name)s,%(email)s, %(address)s, %(city)s, %(state)s, %(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query= 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(db_name).query_db(query, data)
        return results[0]

    classmethod
    def update(data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW(), address = %(address)s, city = %(city)s, state = %(state)s WHERE id = %(id)s;"
        print(data)
        return connectToMySQL(db_name).query_db( query, data )
    
    @classmethod
    def get_oneUser(cls, data):
        query = "select * from users order by updated_at desc limit 1;"
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def is_valid(user):
        is_valid = True
        if not NAME_REGEX.match(user['first_name']):
            flash("Name should have only letters!", "fnameletter")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Name should be at least 2 characters!", "fnamechar")
            is_valid = False
        is_valid = True
        if not NAME_REGEX.match(user['last_name']):
            flash("Last name should be at least 2 characters and should have only letters!", "lnameletter")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name should be at least 2 characters and should have only letters!", "lnamechar")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        query = "select count(email) from users where email = %(email)s;"
        result = connectToMySQL(db_name).query_db(query, user)
        if result[0]['count(email)'] >= 1:
            flash("This email address already exists!", "emailExists")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password should be at least 8 characters!", "password")
            is_valid = False
        if user['confirm'] != user['password']:
            flash("Passwords don't match!", "passwordConfirm")
            is_valid = False
        
        if is_valid == True:
            flash("Success, user created!You can now login!", "userCreated")
        
        return is_valid

    @staticmethod
    def is_valid_update(user):
        is_valid = True
        if not NAME_REGEX.match(user['first_name']) or len(user['first_name']) < 3:
            flash("Name should have only letters, be at least 3 characters and have only letters!", "fnameletter")
            is_valid = False
        # is_valid = True
        if not NAME_REGEX.match(user['last_name']) or len(user['last_name']) < 3:
            flash("Last name should be at least 3 characters and should have only letters!", "lnameletter")
            is_valid = False
        if  len(user['address']) < 3:
            flash("Address should be at least 3 characters and should have only letters!", "address")
            is_valid = False
        if len(user['city']) < 3 :
            flash("City should be at least 3 characters and should have only letters!", "city")
            is_valid = False
        if len(user['state']) < 3 :
            flash("State should be at least 3 characters and should have only letters!", "state")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        query = "select count(email) from users where email = %(email)s;"
        result = connectToMySQL(db_name).query_db(query, user)
        # print(result['email'])
        # if result[0]['count(email)'] >= 1:
        #     # flash("This email address already exists!", "emailExists")
        #     is_valid = False
        if is_valid == True:
            flash("Success, user updated!", "userUpdated")
        return is_valid
        