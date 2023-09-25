import app
from dotenv import dotenv_values
# path to sqlite database
# this will create the db file in instance
# if database not present already
app.config['SQLALCHEMY_DATABASE_URI'] = dotenv_values(".env")
# needed for session cookies
app.config['SECRET_KEY'] = 'MY_SECRET'
# hashes the password and then stores in the database
app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
# allows new registrations to application
app.config['SECURITY_REGISTERABLE'] = True
# to send automatic registration email to user
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False