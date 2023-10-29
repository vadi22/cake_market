from webapp.db import db
from webapp.product.models import Product
from webapp.user.models import User
from sqlalchemy.orm import relationship

class Order(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index = True)
    comment = db.Column(db.String(800))
    user = relationship("User", lazy="joined")
    line = relationship("Order_line", lazy="joined")
    def __repr__(self):
        return '<Order id={} user_id={}>'.format(self.id, self.user_id)

class Order_line(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id), index = True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), index=True)
    quantity = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    # order = relationship("Order", lazy="joined")
    product = relationship("Product", lazy="joined")
    line_status = relationship("Line_status", lazy="joined")
    def __repr__(self):
        return '<Order= {} line={}>'.format(self.order_id, self.id)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True)
    
    def __repr__(self):
        return '<Status id={} name={}>'.format(self.id, self.name)

class Line_status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    line_id = db.Column(db.Integer, db.ForeignKey(Order_line.id), index = True)
    datetime = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey(Status.id), index = True)
    status = relationship("Status", lazy="joined")

    def __repr__(self):
        return '<Line_status {} id={}>'.format(self.status_id, self.id)
    


