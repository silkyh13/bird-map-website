import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import json
from app import app
from bird import Bird
from reset_data import ResetData

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5Eespgmbtct40iOJ@34.69.244.156/bird_database_test'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
 
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

obj = ResetData(app, session)

obj.reset_data()
