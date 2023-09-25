from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
import app

from dotenv import dotenv_values
from dotenv import load_dotenv
load_dotenv()
config = dotenv_values(".env")

engine = create_engine(config['POSTGRESQL_DB'])
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()




