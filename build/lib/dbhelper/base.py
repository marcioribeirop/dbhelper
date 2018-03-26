# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://tevec:ew3wrnaKRy@6D3fyGGtvPGL6tr@172.26.3.122:3306/microservices")
Session = sessionmaker(bind=engine)

Base = declarative_base()