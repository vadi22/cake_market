from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db

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

class User_adress(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(120))
    district = db.Column(db.String(120))
    street = db.Column(db.String(120))
    home = db.Column(db.String(120))
    apartment = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), index=True)

    def __repr__(self):
            return '<User adress id= {} User id={}>'.format(self.id, self.user_id)
        