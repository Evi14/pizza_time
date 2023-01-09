from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logging')
def first_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if User.is_valid(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # print(pw_hash)
        data = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": request.form['email'],
                "address": request.form['address'],
                "city": request.form['city'],
                "state": request.form['state'],
                "password" : pw_hash
        }
        id = User.save(data)
        session['user_id'] = id
        return redirect("/dashboard")
    return redirect("/")
    

@app.route('/orderPizza', methods=['POST'])
def order_pizza():
    if 'user_id' in session:
        data = {
                "user_id":request.form['user_id'],
                "price":request.form['price'],
                "method": request.form['method'],
                "size": request.form['size'],
                "crust": request.form['crust'],
                "quantity": request.form['quantity'],
                "toppings":request.form.getlist('toppings')
        }
        # toppings = {
        #         "user_id":request.form['user_id'],
        #         "toppings":request.form.getlist('toppings')
        # }
        print(data)
        print(data["toppings"])
        Order.saveP(data)
        Order.saveToppings(data["toppings"])
        # Order.toppings(data)
        return redirect("/confirm")
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data))#,recipes=Recipe.get_all()


@app.route('/account')
def editUser():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        # print(user)
        return render_template("editUser.html",loggedUser= user, all_orders=Order.get_all(data))
    return redirect('/loginregister')    

@app.route('/order')
def order():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
    return render_template('order.html', user = User.get_user_by_id(data))


@app.route('/confirm')
def confirm():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('confirm.html', lastOrder = Order.get_last_order(data))
    return render_template('/')


@app.route('/deleteOrder')
def deleteOrder():
    if 'user_id' in session:
        data ={
        'id': session['user_id']
        }
        Order.delete(data)
        return render_template('dashboard.html', user=User.get_by_id(data))
    return render_template('/')


@app.route('/purchase')
def purchase():
    if 'user_id' in session:
        data ={
        'user_id': session['user_id']
        }

        user = User.get_user_by_id(data)
        return render_template("editUser.html",loggedUser= user, all_orders=Order.get_all(data))
    return render_template('/')


@app.route('/update',methods=['POST'])
def updateUser():
    if 'user_id' in session:
        if not User.is_valid_update(request.form):
            return redirect(request.referrer)
        data ={ 
            "id":id
        }
        print(request.form)
        User.update(request.form)
        user = User.get_oneUser(data)
        return redirect('/confirm')    
    return redirect('/logging')  

@app.route('/login', methods=['POST'])
def login():
    # if User.is_valid(request.form):
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "invalidEmail")
        return redirect("/logging")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "invalidEmail")
        return redirect('/logging')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
# never render on a post!!!
    return redirect("/dashboard")

@app.route('/out')
def logout():
    session.clear()
    return redirect("/logging")