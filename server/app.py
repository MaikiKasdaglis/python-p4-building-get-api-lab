#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_list = []
    for bakery in Bakery.query.all():
        bakery_dict = {
         "name": bakery.name,
         "created_at": bakery.created_at,
         "updated_at": bakery.updated_at,
         "id": bakery.id

        }
        bakery_list.append(bakery_dict)
    response = make_response(
       jsonify(bakery_list),
        200,
        {"Content-Type": "application/json"}
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
     
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()
    response = make_response(
       jsonify(bakery_dict),
        200,
        {"Content-Type": "application/json"}
    )
    return response
       

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    return_list = []
    goods_price_list = BakedGood.query.order_by(desc(BakedGood.price)).all()
    for good in goods_price_list:
       new_item = {
            "bakery_id": good.bakery_id,
            "created_at": good.created_at,
            "id": good.id,
            "name": good.name,
            "price": good.price,
            "updated_at": good.updated_at
       }
       return_list.append(new_item)

    response = make_response(
       jsonify(return_list),
        200,
        {"Content-Type": "application/json"}
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    
    spensive = BakedGood.query.order_by(desc(BakedGood.price)).first()
    new_item = {
        "bakery_id": spensive.bakery_id,
        "created_at": spensive.created_at,
        "id": spensive.id,
        "name": spensive.name,
        "price": spensive.price,
        "updated_at": spensive.updated_at
    }
    
    response = make_response(
       jsonify(new_item),
        200,
        {"Content-Type": "application/json"}
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
