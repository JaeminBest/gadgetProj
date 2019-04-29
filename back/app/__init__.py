# __init__.py
# author : jaemin kim
# details : back-end server setting that INSERT original image data in db

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://inspector:inspector@localhost/inspector_db?charset=utf8mb4&binary_prefix=true"', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'
CORS(app)   # for react parameter passing
