from dotenv import dotenv_values
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()
config = dotenv_values(".env")
print(config)
SQLALCHEMY_DATABASE_URI = 'postgresql://vnfswgnb:ypVRcYVSfjmUj_bdz4q4yeuAT7FMBRge@snuffleupagus.db.elephantsql.com/vnfswgnb' #не понимаю почему не могу достать, наверное из-за того что есть config.py
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'MY_SECRET'
SQLALCHEMY_TRACK_MODIFICATIONS = False

