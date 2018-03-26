from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text, Boolean

from dbhelper.utils.connection import ConnectionSQL as connection


class StructureDatabase(object):

    def __init__(self):
        self.structure_model()
        self.structure_app()
        self.structure_client()
        self.structure_model_meta_data()

    def structure_model(self):
        metadata = MetaData()
        model = Table('models', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('model_source', Text()))

        model.create(connection)

    def structure_app(self):
        metadata = MetaData()
        app = Table('app', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(30)),
                      Column('base_route', String(30)))

        app.create(connection)

    def structure_client(self):
        metadata = MetaData()
        client = Table('client', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(30)))

        client.create(connection)

    def structure_model_meta_data(self):
        metadata = MetaData()
        model_meta_data = Table('model_meta_data', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('model_id', Integer, ForeignKey('model.id')),
                    Column('app_id', Integer, ForeignKey('app.id')),
                    Column('client_id', Integer, ForeignKey('client.id')),
                    Column('version', String(6)),
                    Column('product', String(30)),
                    Column('io_template', Text()),
                    Column('active', Boolean()))

        model_meta_data.create(connection)