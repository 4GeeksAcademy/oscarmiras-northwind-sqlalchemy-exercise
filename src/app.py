"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Product, Supplier, Order, OrderDetail
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

def create_product():
    product = Product(product_name="Mandarina", list_price=1.1)
    # encolo el producto que quiero crear en base de datos
    db.session.add(product)
    # Confirmo los cambios para que haga los INSERT
    db.session.commit()
    
def get_product(id):
    product = Product.query.get(id)
    print(product)

def get_all_products():
    products = Product.query.all()
    for p in products:
        print(p)

# productos que valen menos de 1.3 €
def get_cheap_products():
    # De todos los productos que me develve esta query filtrada, los quiero todos (me dará una lista)
    products = Product.query.filter(Product.list_price < 1.3).all()
    for p in products:
        print(p)

def get_all_products_of_a_single_supplier(id):
    # Obtengo el supplier que tiene esta id
    supplier = Supplier.query.get(id)

    # Tengo una propiedad, de nombre 'products', que contiene todos los productos de los que soy proveedor
    print(f'Productos para la compañia: {supplier.company_name}')
    for p in supplier.products:
        print(p)


def insert_suppliers():
    cocacola = Supplier(company_name='Coca Cola', homepage='https://cocacola.com')
    db.session.add(cocacola)
    fruitco = Supplier(company_name='Fruits Company', homepage='https://piñacolada.com')
    db.session.add(fruitco)
    db.session.commit()

def create_order(city):
    order = Order(ship_city=city)
    db.session.add(order)
    db.session.commit()

# Añadir un producto a una orden de compra
def add_to_cart(o_id, p_id):
    # order_id es el nombre de la columna
    # o_id simplemente es el valor del parámetro de la función
    od = OrderDetail(order_id=o_id, product_id = p_id)
    db.session.add(od)
    db.session.commit()

# Muestrame todos los productos de una orden de compra
def get_products_from_order(o_id):
    order = Order.query.get(o_id)
    for detail in order.orderdetails:
        print(detail)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    # app.run(host='0.0.0.0', port=PORT, debug=False)

    # Lo necesitamos para pdoer ejecutar código Python normal fuera del entorno de Flask
    with app.app_context():
        #create_product()
        # get_product(2)
        # get_all_products()
        # get_cheap_products()
        # insert_suppliers()
        # get_all_products_of_a_single_supplier(2)
        #add_to_cart(1, 1)
        #add_to_cart(1, 5)
        get_products_from_order(1)
        


