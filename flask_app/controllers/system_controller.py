from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.model.user_model import User
from flask_app.model.car_model import Car 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['txtPword'])
    print (pw_hash)
    data = {
        "email": request.form["txtEmail"]
    }
    user_email = User.verify_user(data)
    if user_email:
        flash('E-Mail Address already registered!')
        return redirect('/')
    data = {
        "fname": request.form["txtFname"],
        "lname": request.form["txtLname"],
        "email": request.form["txtEmail"],
        "pword": pw_hash
    }
    
    flash('Account Successfully Registered!')
    User.save_user(data)
    return redirect('/')

@app.route('/dashboard', methods=["POST"])
def login_user():
    if not User.validate_login(request.form):
        return redirect('/')

    data = {
        "email": request.form["txtEmail"],
        "pword": request.form["txtPword"]
    }
    user = User.verify_user(data)
    if not user:
        flash ('Wrong E-Mail or Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['txtPword']):
        flash ('Wrong E-Mail or Password')
        return redirect('/')
    session['user_id'] = user.id
    session['firstname'] = user.firstname
    return redirect('/main_page')

@app.route('/save_car', methods=["POST"])
def save_car():
    if not Car.validate_car(request.form):
        return redirect('/new_car')
    data={
        "users_id" : session['user_id'],
        "price" : request.form['txtCarPrice'],
        "model" : request.form['txtCarModel'],
        "make" : request.form['txtCarMake'],
        "year" : request.form['txtCarYear'],
        "description" : request.form['txtCarDescription']
    }
    Car.add_car(data)
    return redirect('/main_page')

@app.route('/update_car', methods=["POST"])
def update_car():
    if not Car.validate_car(request.form):
        car_id = session['car_id']
        return redirect('/edit_car/'+str(car_id))
    data={
        "car_id" : session['car_id'],
        "price" : request.form['txtCarPrice'],
        "model" : request.form['txtCarModel'],
        "make" : request.form['txtCarMake'],
        "year" : request.form['txtCarYear'],
        "description" : request.form['txtCarDescription']
    }
    Car.update_car(data)
    return redirect('/main_page')

@app.route('/purchase_car', methods=["POST"])
def purchase_car():
    data={
        "user_id" : session['user_id'],
        "car_id" : session['car_id'],
    }
    Car.purchase_car(data)
    return redirect('/main_page')

@app.route('/view_car/<int:car_id>')
def view_car(car_id):
    data = {
        "car_id" : car_id
    }
    session['car_id'] = car_id
    car = Car.display_car_details(data)
    return render_template("show_car.html", car_details = car)

@app.route('/edit_car/<int:car_id>')
def edit_car(car_id):
    data = {
        "car_id" : car_id
    }
    session['car_id'] = car_id
    car = Car.edit_car(data)
    return render_template("edit_car.html", car_details = car)

@app.route('/delete_car/<int:car_id>')
def delete_car(car_id):
    data = {
        "car_id" : car_id
    }
    car = Car.delete_car(data)
    return redirect('/main_page')

@app.route('/list_purchased_car')
def list_purchased_car():
    data = {
        "user_id" : session['user_id']
    }
    cars = Car.list_purchased_car(data)
    return render_template("purchased_car.html",list_of_cars = cars )


@app.route('/main_page')
def main_page():
    cars = Car.get_all_cars()
    return render_template("dashboard.html", list_of_cars = cars)

@app.route('/new_car')
def new_car():
    return render_template("add_car.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('fname', None)
    return redirect('/')