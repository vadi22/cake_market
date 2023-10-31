import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRESQL_DB")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'MY_SECRET'
SQLALCHEMY_TRACK_MODIFICATIONS = False
REMEMBER_COOKIE_DURATION = timedelta(days=5)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'marketcake260@gmail.com'
MAIL_PASSWORD = 'qgwz bnqo cuhq uvdm'
MAIL_DEFAULT_SENDER = 'marketcake260@gmail.com'