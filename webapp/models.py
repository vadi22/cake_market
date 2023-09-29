from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username =db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    telegram_id = db.Column(db.String(120), index = True, unique = True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
















