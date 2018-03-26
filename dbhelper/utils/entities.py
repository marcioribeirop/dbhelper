from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, PickleType
from sqlalchemy.orm import relationship
from dbhelper.base import Base


class Model(Base):

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    model_source = Column('model_source', PickleType())

    def __init__(self, model_source):
        self.model_source = model_source


class App(Base):

    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True)
    name = Column('name', Text)

    def __init__(self, name):
        self.name = name


class Client(Base):

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30))

    def __init__(self, name):
        self.name = name


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30))

    def __init__(self, name):
        self.name = name


class ModelMetaData(Base):

    __tablename__ = 'models_meta_data'

    id = Column(Integer, primary_key=True)
    model_id = Column('model_id', Integer, ForeignKey('models.id'))
    app_id = Column('app_id', Integer, ForeignKey('apps.id'))
    client_id = Column('client_id', Integer, ForeignKey('clients.id'))
    product_id = Column('product_id', Integer, ForeignKey('products.id'))
    version = Column('version', String(6))
    io_template = Column('io_template', PickleType())
    active = Column('active', Boolean())
    model_name = Column('model_name', Text())

    model = relationship("Model")
    app = relationship("App")
    client = relationship("Client")
    product = relationship("Product")

    def __init__(self, model_id, app_id, client_id, version, product_id, io_template, active, model_name):
        self.model_id = model_id
        self.app_id = app_id
        self.client_id = client_id
        self.version = version
        self.product_id = product_id
        self.io_template = io_template
        self.active = active
        self.model_name = model_name