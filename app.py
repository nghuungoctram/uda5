import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import setup_db, Shirt, Customer
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


# --------------------------------------------------
# SHIRT API
# --------------------------------------------------
# GET ALL SHIRT
@app.route('/shirts', methods=['GET'])
@cross_origin()
def get_shirt_method():
    return jsonify(
        success=True,
        shirt=[shirt.format() for shirt in (Shirt.query.all())]
    ), 200


# ADD NEW SHIRT
@app.route('/shirt', methods=['POST'])
@requires_auth('post:shirt')
def new_shirt_method(param):
    body = request.get_json()

    if (body.get('name', None) is None):
        abort(400, 'shirt not found or not added')

    shirt = Shirt(name=body.get('name', None), color=body.get('color', None),
                  size=body.get('size', None), link=body.get('link', None))
    shirt.insert()

    return jsonify({
        'success': True,
        'id': shirt.id,
        'shirtName': shirt.name,
    }), 200


# UPDATE SHIRT INFORMATION BY ID
@app.route('/shirt/<int:id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:shirt')
def update_shirt_method(payload, id):
    shirt = Shirt.query.filter(Shirt.id == id).one_or_none()
    body = request.get_json()

    if shirt is None:
        abort(404, 'Shirt not found')

    else:
        shirt.name = body.get('name', None)
        shirt.color = body.get('color', None)
        shirt.size = body.get('size', None)
        shirt.link = body.get('link', None)

        shirt.update()

    return jsonify({
        'success': True,
        'shirt': shirt.format()
    }), 200


# DELETE SHIRT
@app.route('/shirt/<int:id>', methods=['DELETE'])
@requires_auth('delete:shirt')
def delete_shirt_method(payload, id):
    shirt = Shirt.query.filter(Shirt.id == id).one_or_none()

    if (shirt is None):
        abort(404, 'Shirt not found')
    else:
        shirt.delete()

    return jsonify(
        success=True,
        delete=id
    ), 200


# --------------------------------------------------
# CUSTOMER API
# --------------------------------------------------
# GET ALL CUSTOMER
@app.route('/customers', methods=['GET'])
def get_customer_method():
    return jsonify(
        success=True,
        shirt=[customer.format() for customer in (Customer.query.all())]
    ), 200


# ADD NEW CUSTOMER
@app.route('/customer', methods=['POST'])
@requires_auth('post:customer')
def new_customer_method(param):
    body = request.get_json()

    if (body.get('name', None) is None):
        abort(400, 'customer not found')

    customer = Customer(name=body.get('name', None), gender=body.get('gender', None),
                        phone=body.get('phone', None), shirt_id=body.get('shirt_id', None))
    customer.insert()

    return jsonify({
        'success': True,
        'id': customer.id,
        'customerName': customer.name,
    }), 200


# UPDATE CUSTOMER INFORMATION BY ID
@app.route('/customer/<int:id>', methods=['PATCH'])
@requires_auth('patch:customer')
def update_customer_method(payload, id):
    customer = Customer.query.filter(Customer.id == id).one_or_none()
    body = request.get_json()

    if customer is None:
        abort(404, 'Customer not found')

    else:
        customer.name = body.get('name', None)
        customer.gender = body.get('gender', None)
        customer.phone = body.get('phone', None)
        customer.shirt_id = body.get('shirt_id', None)

        customer.update()

    return jsonify({
        'success': True,
        'customer': customer.format()
    }), 200


# DELETE CUSTOMER
@app.route('/customer/<int:id>', methods=['DELETE'])
@requires_auth('delete:customer')
def delete_customer_method(payload, id):
    customer = Customer.query.filter(Customer.id == id).one_or_none()

    if (customer is None):
        abort(404, 'customer not found')
    else:
        customer.delete()

    return jsonify(
        success=True,
        delete=id
    ), 200


# Error Handling
@app.errorhandler(400)
def bad_request_error(er):
    return jsonify({
        'success': False,
        'error': 'Bad Request',
        "message": "got Bad request error"
    }), 400


@app.errorhandler(404)
def page_not_found_error(er):
    return jsonify({
        "success": False,
        'error': 404,
        "message": "Page Not Found or File Not Found"
    }), 404


@app.errorhandler(405)
def invalid_method_error(er):
    return jsonify({
        "success": False,
        'error': 405,
        "message": "method not allowed!"
    }), 405


@app.errorhandler(422)
def unprocessable_entity_error(er):
    return jsonify({
        "success": False,
        'error': 422,
        "message": "Unprocessable entity error"
    }), 422


@app.errorhandler(500)
def server_error(er):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error/Temporary Error'
    }), 500


@app.errorhandler(AuthError)
def authen_got_fail(er):
    return jsonify({
        "success": False,
        "error": er.status_code,
        "message": "Authentification is not successful"
    }), 401


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
