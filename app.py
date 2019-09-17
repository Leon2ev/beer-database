import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Connection to MongoDB

app.config["MONGO_DBNAME"] = 'beer_brewing'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/home_page')
def home_page():
    """ Home page """
    return render_template("index.html",
    types=mongo.db.types.find())



@app.route('/get_products')
def get_products():
    """ Page with all products """
    return render_template("products.html",
                            types=mongo.db.types.find(),
                            products=mongo.db.products.find())


@app.route('/get_description/<product_id>')
def get_description(product_id):
    """ Single product description """
    return render_template("description.html",
                            brands=mongo.db.brands.find(),
                            types=mongo.db.types.find(),
                            product=mongo.db.products.find_one({"_id": ObjectId(product_id)}))   


@app.route('/add_product')
def add_product():
    """ Add product """
    return render_template("addproduct.html",
                            brands=mongo.db.brands.find(),
                            types=mongo.db.types.find())

    
@app.route('/insert_product', methods=["POST"])
def insert_product():
    """ Proceed data from form to db """
    products=mongo.db.products
    brand_id = request.form.get('brand_id')
    type_id = request.form.get('type_id')
    gluten_free = request.form.get('gluten_free')
    dictionary = {
        'name': request.form.get('name'),
        'brand_id': ObjectId(brand_id),
        'image_url': request.form.get('image_url'),
        'type_id': ObjectId(type_id),
        'about': request.form.get('about'),
        'abv': request.form.get('abv'),
        'amount': request.form.get('amount'),
    }
    products.insert_one(dictionary)
    return redirect(url_for('get_products'))
    

@app.route('/edit_product/<product_id>')
def edit_product(product_id):
    """ Edit product form """
    return render_template("editproduct.html",
                            product=mongo.db.products.find_one({"_id": ObjectId(product_id)}),
                            brands=mongo.db.brands.find(),
                            types=mongo.db.types.find())

# Update product

@app.route('/update_product/<product_id>', methods=["POST"])
def update_product(product_id):
    """ Update product information in db """
    products=mongo.db.products
    brand_id=request.form.get('brand_id')
    type_id=request.form.get('type_id')
    products.update({'_id': ObjectId(product_id)},
    {
        'name': request.form.get('name'),
        'brand_id': ObjectId(brand_id),
        'image_url': request.form.get('image_url'),
        'type_id': ObjectId(type_id),
        'about': request.form.get('about'),
        'abv': request.form.get('abv'),
        'amount': request.form.get('amount'),
    })
    return redirect(url_for('get_products'))
    

@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    """ Delete choosen product """
    mongo.db.products.remove({'_id': ObjectId(product_id)})
    return redirect(url_for('get_products'))


@app.route('/get_brands')
def get_brands():
    """ Brand page """
    return render_template("brands.html", 
                            brands=mongo.db.brands.find())


@app.route('/add_brand')
def add_brand():
    """ Add brand form """
    return render_template("addbrand.html")


    
@app.route('/insert_brand', methods=["POST"])
def insert_brand():
    """ Proceed data from form to db """
    brands=mongo.db.brands
    brands.insert_one(request.form.to_dict())
    return redirect(url_for('get_brands'))
    

@app.route('/edit_brand/<brand_id>')
def edit_brand(brand_id):
    """ Edit brand form """
    return render_template("editbrand.html",
                            brand=mongo.db.brands.find_one({"_id": ObjectId(brand_id)}))


@app.route('/update_brand/<brand_id>', methods=["POST"])
def update_brand(brand_id):
    """ Update product information in db """
    brands=mongo.db.brands
    brands.update({'_id': ObjectId(brand_id)},
    {
        'name': request.form.get('name'),
        'country': request.form.get('country'),
        'website_URL': request.form.get('website_URL'),
        'instruction_URL': request.form.get('instruction_URL'),
    })
    return redirect(url_for('get_brands'))


@app.route('/delete_brand/<brand_id>')
def delete_brand(brand_id):
    mongo.db.brands.remove({'_id': ObjectId(brand_id)})
    return redirect(url_for('get_brands'))

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
