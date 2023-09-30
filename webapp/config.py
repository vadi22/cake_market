import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRESQL_DB") 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'MY_SECRET'
SQLALCHEMY_TRACK_MODIFICATIONS = False

