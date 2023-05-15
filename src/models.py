from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # columna de nombre product_name, será un string de 120 carácteres como máximo y siempre que cree un producto tengo que informar de este valor
    product_name = db.Column(db.String(120), nullable=False)

    # el precio del producto
    list_price = db.Column(db.Float, nullable=False)

    #Todo producto es entrega por un proveedor (supplier)
    # Nombre columna es arbitrario, pero por convencción, ponemos el nombre de la tabla que está relacionado_id
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=True)

    # Esto me va permitir navegar de este producto a su provedor. De esta manera, puedo obtener el nombre del provedor, su homepage, en general, cualquier columna de esa otra tabla
    # backref : es un parámetro opcional pero recomendable que nos va a permitir hacer la negación inveersa. Desde Supplier, yo voy a poder navegar a los productos que dicho proveedor suministra. Siempre que usemos Flask, ponedlo.
    # Esto es puramente algo de SQLAlchemy
    supplier = relationship('Supplier', backref='products')



    def __repr__(self):
        return f'<Product {self.product_name} - {self.list_price} € y pertenece al proveedor {self.supplier.company_name}>'


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name =  db.Column(db.String(120),unique=True, nullable=False)
    # Aún hay empresas sin página Web...
    homepage = db.Column(db.String(120))

    def __repr__(self):
        return f'<Supplier {self.company_name}'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ship_city = db.Column(db.String(80), nullable=False)

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # En backref ponemos el nombre de la tabla, en minúsculas y en plural
    order = relationship('Order', backref='orderdetails')
    product = relationship('Product', backref='orderdetails')

    def __repr__(self):
        return f'{self.product.product_name} - {self.order.ship_city}'