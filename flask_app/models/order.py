from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db_name = 'pizza'
class Order:
    db_name = "pizza"
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.method = data['method']
        self.crust = data['crust']
        self.size = data['size']
        self.quantity = data['quantity']
        self.created_at = data['created_at']

    @classmethod
    def saveP(cls,data):
        query = "INSERT INTO pizzas (user_id,price, method, crust, size, quantity) VALUES (%(user_id)s,%(price)s, %(method)s, %(crust)s, %(size)s, %(quantity)s);"
        return connectToMySQL(db_name).query_db(query,data)

    # @classmethod
    # def saveToppings(cls,varlist):
    #     # query = "INSERT INTO favorites (user_id,topping_id) VALUES (%(author_id)s,%(book_id)s);"
        
    #     # varlist = [variable_1,variable_2]
    #     var_string = ', '.join('?' * len(varlist))
    #     query_string = 'INSERT INTO pizzas_has_toppings (pizza_id,topping_id) VALUES (%s, %()s);' % var_string
    #     cursor.execute(query_string, varlist)
    #     return connectToMySQL(db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM pizzas WHERE user_id = %(user_id)s"
        orders = []
        results = connectToMySQL(db_name).query_db(query,data)
        for row in results:
            orders.append(cls(row))
        return orders

    @classmethod
    def delete(cls,data):
        query = "Delete FROM pizza.pizzas where user_id = %(id)s ORDER BY id DESC limit 1;"
        return connectToMySQL(db_name).query_db(query,data)

    @classmethod
    def get_last_order(cls, data):
        query = "SELECT * FROM pizzas WHERE user_id = %(user_id)s ORDER BY id DESC limit 1"
        # authors = []
        results = connectToMySQL(db_name).query_db(query,data)
        return results

