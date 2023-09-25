from dotenv import dotenv_values
from sqlalchemy import create_engine
import app

config = dotenv_values(".env")
SQLALCHEMY_DATABASE_URI =  create_engine(config['POSTGRESQL_DB'])

SQLALCHEMY_DATABASE_URI= create_engine(config['POSTGRESQL_DB'])        
# needed for session cookies
SECRET_KEY = 'MY_SECRET'
# hashes the password and then stores in the database
SECURITY_PASSWORD_SALT = "MY_SECRET"
# allows new registrations to application
SECURITY_REGISTERABLE = True
# to send automatic registration email to user
SECURITY_SEND_REGISTER_EMAIL = False


# app.config['SQLALCHEMY_DATABASE_URI'] = 
# # needed for session cookies
# app.config['SECRET_KEY'] = 'MY_SECRET'
# # hashes the password and then stores in the database
# app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
# # allows new registrations to application
# app.config['SECURITY_REGISTERABLE'] = True
# # to send automatic registration email to user
# app.config['SECURITY_SEND_REGISTER_EMAIL'] = False