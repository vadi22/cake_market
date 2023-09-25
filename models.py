from flask_security import UserMixin, RoleMixin
# from sqlalchemy import Column, Integer, String, Table, Boolean, ForeignKey
from db import engine, Base
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import app
from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore



db = SQLAlchemy()
db.init_app(app)
 
# runs the app instance
app.app_context().push()
 
# create table in database for assigning roles
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))   
 
# create table in database for storing users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # backreferences the user_id from roles_users table
    active = db.Column(db.Boolean())
    # backreferences the user_id from roles_users table
    roles = relationship('Role', secondary=roles_users, backref='roled')
    telegram_id = db.Column(db.Integer, primary_key=True)
 
# create table in database for storing roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
     
# creates all database tables
# @app.before_first_request
# def create_tables():
#     db.create_all()

# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)

@app.before_first_request
def create_tables():
    db.create_all()


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)