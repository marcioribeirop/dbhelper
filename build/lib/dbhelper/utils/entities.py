from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from dbhelper.base import Base


class Model(Base):

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    model_source = Column('model_source', Text)

    def __init__(self, model_source):
        self.model_source = model_source


class App(Base):

    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True)
    name = Column('model_source', Text)
    base_route = Column('base_route', String(30))

    def __init__(self, name, base_route):
        self.name = name
        self.base_route = base_route


class Client(Base):

    __tablename__ = 'clients'

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
    requirements = Column('requirements', Text())
    version = Column('version', String(6))
    product = Column('product', String(30))
    io_template = Column('io_template', Text())
    active = Column('active', Boolean())

    model = relationship("Model")
    app = relationship("App")
    client = relationship("Client")

    def __init__(self, model_id, app_id, client_id, requirements, version, product, io_template, active):
        self.model_id = model_id
        self.app_id = app_id
        self.client_id = client_id
        self.requirements = requirements
        self.version = version
        self.product = product
        self.io_template = io_template
        self.active = active