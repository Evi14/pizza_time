from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/orderPizza', methods=['POST'])
def order_pizza():
    if 'user_id' in session:
        data = {
                "method": request.form['first_name'],
                "size": request.form['last_name'],
                "crust": request.form['email'],
                "quantity": request.form['address'],
        }
        id = Order.save(data)
        session['user_id'] = id
        return redirect("/dashboard")
    return redirect("/")

