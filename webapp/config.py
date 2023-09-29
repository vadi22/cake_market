from dotenv import dotenv_values
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()
config = dotenv_values(".env")
print(config)
SQLALCHEMY_DATABASE_URI = config['POSTGRESQL_DB'] #не понимаю почему не могу достать, наверное из-за того что есть config.py
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
   
# needed for session cookies
SECRET_KEY = 'MY_SECRET'
# hashes the password and then stores in the database
SECURITY_PASSWORD_SALT = "MY_SECRET"
# allows new registrations to application
SECURITY_REGISTERABLE = True
# to send automatic registration email to user
SECURITY_SEND_REGISTER_EMAIL = False

