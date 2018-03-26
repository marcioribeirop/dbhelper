from dbhelper.base import Base, engine
from dbhelper.utils.entities import Model, App, Client, ModelMetaData, Product


class CreateSchema(object):

    def __init__(self):
        Base.metadata.create_all(engine)