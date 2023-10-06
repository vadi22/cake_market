from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password =db.Column(db.String(128), index = True, unique = True)
    active = db.Column(db.Boolean())
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    telegram_id = db.Column(db.String(120), index = True, unique = True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        return self.role == 1 and self.active

    def __repr__(self):
        return '<Email= {} id={}>'.format(self.email, self.id)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.String(400))
    labor_id = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Product= {} id={}>'.format(self.name, self.id)
    
class Component(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.String(400))
    
    def __repr__(self):
        return '<Component {} id={}>'.format(self.name, self.id)
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(120), unique = True)
    
    def __repr__(self):
        return '<Image id={} link={}>'.format(self.id, self.link)
    
class Price(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    component_id = db.Column(db.Integer, index = True)
    cost = db.Column(db.Numeric(7,2))
    discount = db.Column(db.Numeric(3,2))

    def __repr__(self):
        return '<Price id={} component_id={} cost={} discount={}>'.format(self.id, self.component_id, self.cost, self.discount)
    
class Labor(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    hours = db.Column(db.Numeric(3,2))
    cost = db.Column(db.Numeric(7,2))

    def __repr__(self):
        return '<Labor id={} hours={} cost={}>'.format(self.id, self.hours, self.cost)
    
class Product_Component(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, index = True)
    component_id = db.Column(db.Integer, index = True)
    
    def __repr__(self):
        return '<Product_Component id={}>'.format(self.id)

class Product_Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, index = True)
    image_id =db.Column(db.Integer, index = True)
    
    def __repr__(self):
        return '<Product_Image id={}>'.format(self.id)

class Component_Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    component_id = db.Column(db.Integer, index = True)
    image_id =db.Column(db.Integer, index = True)
    
    def __repr__(self):
        return '<Component_Image id={}>'.format(self.id)














