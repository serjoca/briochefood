from app import db


class Bakery(db.Model):
    __tablename__ = "bakeries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    recipient_id = db.Column(db.String(256), index=True)
    
    products = db.relationship("Product")
    
    def __repr__(self):
        return f"<Bakery {self.name}>"

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    price = db.Column(db.Float)
    
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    bakery = db.relationship("Bakery")

    def __repr__(self):
        return f"<Product {self.name}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float)
    transaction_id = db.Column(db.String(256))
    status = db.Column(db.String(256))
    
    items = db.relationship("OrderDetails")
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    bakery = db.relationship("Bakery")

    def __repr__(self):
        return f"<Order {self.id} {self.bakery_id} >"

class OrderDetails(db.Model):
    __tablename__ = "order_details"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderDetails {self.order_id} {self.product_id} >"
