from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeSerializer as Serializer
from datetime import datetime
from sqlalchemy.orm import relationship
from webapp.db import db
from webapp import config


ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password =db.Column(db.String(128), index = True, unique = True)
    active = db.Column(db.Boolean(), default = True )
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    telegram_id = db.Column(db.String(120), index = True, unique = True)
    address = relationship("User_adress", lazy="joined")

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_token(self):
         serial= Serializer(config.SECRET_KEY)
         print(serial.dumps({'user_id':self.id}))
         return serial.dumps({'user_id':self.id})
    
    @staticmethod     
    def verify_token(token):
        serial = Serializer(config.SECRET_KEY)
        try:
            user_id = serial.loads(token)['user_id']
        except:
             return None
        return User.query.get(user_id)
         
    @property
    def is_admin(self):
        return self.role == 1 and self.active

    def __repr__(self):
        return '<Email= {} id={}>'.format(self.email, self.id)

class User_adress(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(120), default = '-')
    district = db.Column(db.String(120), default = '-')
    street = db.Column(db.String(120), default = '-')
    home = db.Column(db.String(120), default = '-')
    apartment = db.Column(db.String(120), default = '-')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), index=True)

    def __repr__(self):
            return '<User adress id= {} User id={}>'.format(self.id, self.user_id)
        

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'),  index=True) 
    user = relationship('User', backref='reviews')
 



    def __repr__(self):
        return '<Review {}>'.format(self.id)