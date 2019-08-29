import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Connection to MongoDB

app.config["MONGO_DBNAME"] = 'beer_brewing'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

# App routes

@app.route('/')
@app.route('/get_products')
def get_products():
    return render_template("products.html", 
    products=mongo.db.products.find())

@app.route('/add_product')
def add_product():
    return render_template("addproduct.html",
    brands=mongo.db.brands.find(),
    types=mongo.db.types.find())
    
@app.route('/insert_product', methods=["POST"])
def insert_product():
    products=mongo.db.products
    products.insert_one(request.form.to_dict())
    return redirect(url_for('get_products'))
    
@app.route('/get_description')
def get_description():
    return render_template("description.html", 
    products=mongo.db.products.find(),
    brands=mongo.db.brands.find())

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
