#creating a flask sqlalchemy api for a database project
from flask import Flask,render_template,jsonify,json,request
from flask_restful import Api,reqparse,Resource,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests,os

#initializing our sqlalchemy and api modules
app = Flask(__name__)
#init api object
api = Api(app)
#init db
db = SQLAlchemy(app)
#init marshmallow
marsh = Marshmallow(app)
#init base directory
basedir = os.path.abspath(os.path.dirname(__file__))
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'Flask_Api_Database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/',methods=['GET'])
def get():
    return jsonify({'message':'Hello Louis,this is a flask Api in Working.'})

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    prod_name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self,prod_name,description,price,quantity):
        self.prod_name = prod_name
        self.description = description
        self.price = price
        self.quantity = quantity

#create product schema class
class ProductSchema(marsh.Schema):
    class Meta:
        fields = ('id','prod_name','description','price','quantity')

#init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
@app.route('/product',methods=['POST'])
def put():
    prod_name = request.json['prod_name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    new_product = Product(prod_name,description,price,quantity)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

#get all products
@app.route('/product',methods=['GET'])
def get_all():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

#get single product
@app.route('/product/<id>',methods=['GET'])
def get_single(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#update a product
@app.route('/product/<id>',methods=['PUT'])
def update(id):
    product = Product.query.get(id)
    prod_name = request.json['prod_name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product.prod_name = prod_name
    product.description = description
    product.price = price
    product.quantity = quantity
    db.session.commit()
    return product_schema.jsonify(product)

#deleting product(s)
@app.route('/product/<id>',methods=['DELETE'])
def del_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)