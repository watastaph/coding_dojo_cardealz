from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model import user_model
from flask import flash,session

class Car:
    def __init__( self , data ):
        self.id = data['id']
        self.users_id = data['users_id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller= None
        self.buyer= []


    @staticmethod 
    def validate_car(car):
        is_valid=True
        if len(car['txtCarPrice'])<= 0  or len(car['txtCarPrice'])<=0 or len(car['txtCarMake'])<=0 or len(car['txtCarYear'])<=0 or len(car['txtCarDescription'])<=0:
            flash("Please fill-out the necessary fields!")
            is_valid=False
        elif int(car['txtCarPrice']) <=0 and int(car['txtCarYear']) <=0:
            flash("Price and Year must be greater than 0!")
            is_valid=False
        return is_valid

    @classmethod
    def add_car(cls, data):
        query = "INSERT INTO cars (users_id, price, model, make, year, description, created_at, updated_at) VALUES (%(users_id)s,%(price)s,%(model)s,%(make)s,%(year)s,%(description)s, NOW(), NOW());"
        return connectToMySQL('db').query_db( query, data )
    
    @classmethod
    def get_all_cars(cls):
        query="SELECT * FROM cars LEFT JOIN users ON cars.users_id = users.id LEFT JOIN purchases on cars.id = purchases.cars_id"
        results = connectToMySQL('db').query_db(query)
        this_user = []
        for row_from_db in results:
            buyer_data = {
                "id" : row_from_db['purchases.users_id'],
                "lastname" : row_from_db['lastname'],
                "firstname" : row_from_db['firstname'],
                "email" : row_from_db['email'],
                "password" : row_from_db['password'],
                "created_at" : row_from_db['purchases.created_at'],
                "updated_at" : row_from_db['purchases.updated_at']
            }
            if len(this_user)>0 and this_user[len(this_user)-1].id == row_from_db['users_id']:
                this_user[len(this_user)-1].buyer.append(user_model.User(buyer_data))

            else:
                new_car = cls(row_from_db)
                seller_data = {
                    "id" : row_from_db['users.id'],
                    "lastname" : row_from_db['lastname'],
                    "firstname" : row_from_db['firstname'],
                    "email" : row_from_db['email'],
                    "password" : row_from_db['password'],
                    "created_at" : row_from_db['users.created_at'],
                    "updated_at" : row_from_db['users.updated_at']
                }
                seller = user_model.User(seller_data)
                new_car.seller = seller
                if row_from_db['purchases.users_id'] is not None:
                    new_car.buyer.append(user_model.User(buyer_data))
                this_user.append(new_car)
                print(this_user)
        return this_user

    @classmethod
    def display_car_details(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.users_id = users.id WHERE cars.id=%(car_id)s;"
        results = connectToMySQL('db').query_db(query, data)
        
        cars = []
        for row_from_db in results:
            seller_data = {
                "id" : row_from_db['users_id'],
                "price" : row_from_db['price'],
                "model" : row_from_db['model'],
                "description" : row_from_db['description'],
                "year" : row_from_db['year'],
                "make" : row_from_db['make'],
                "lastname" : row_from_db['lastname'],
                "firstname" : row_from_db['firstname'],
                "email" : row_from_db['email'],
                "password" : row_from_db['password'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at']
            }
            cars.append(seller_data)
            print(cars)
        return cars

    @classmethod
    def purchase_car(cls, data):
        query = "INSERT INTO purchases (users_id, cars_id, status, created_at, updated_at) VALUES (%(user_id)s, %(car_id)s,'SOLD', NOW(), NOW());"
        print(query)
        return connectToMySQL('db').query_db( query, data )

    @classmethod
    def edit_car(cls, data):
        query = "SELECT * FROM cars WHERE id = %(car_id)s;"
        results = connectToMySQL('db').query_db(query, data)
        cars = []
        for car in results:
            cars.append( cls(car) )
        print(cars)
        return cars

    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars  SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s,  updated_at = NOW() WHERE id=%(car_id)s;"
        return connectToMySQL('db').query_db( query, data )

    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id=%(car_id)s;"
        return connectToMySQL('db').query_db( query, data )
    
    @classmethod
    def list_purchased_car(cls, data):
        query = "SELECT * FROM purchases LEFT JOIN cars ON purchases.cars_id = cars.id WHERE purchases.users_id = %(user_id)s;"
        results = connectToMySQL('db').query_db(query, data)
        cars = []
        for row_from_db in results:
            seller_data = {
                "model" : row_from_db['model'],
                "year" : row_from_db['year'],
                "make" : row_from_db['make']
            }
            cars.append(seller_data)
            print(results)
        return cars