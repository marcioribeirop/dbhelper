from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text, Boolean
from dbhelper.dbhelper_connector import DBHelper


class StructureDatabase(DBHelper):

    def __init__(self):
        super().__init__()

        metadata = MetaData()

        self.structure_model(metadata)
        self.structure_app(metadata)
        self.structure_client(metadata)
        self.structure_model_meta_data(metadata)

    def structure_model(self, metadata):
        model = Table('model', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('model_source', Text()))

        model.create(self.conn)

    def structure_app(self, metadata):
        app = Table('app', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(30)),
                      Column('base_route', String(30)))

        app.create(self.conn)

    def structure_client(self, metadata):
        client = Table('client', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(30)))

        client.create(self.conn)

    def structure_model_meta_data(self, metadata):
        model_meta_data = Table('model_meta_data', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('model_id', Integer, ForeignKey('model.id')),
                    Column('app_id', Integer, ForeignKey('app.id')),
                    Column('client_id', Integer, ForeignKey('client.id')),
                    Column('requirements', Text()),
                    Column('version', String(6)),
                    Column('product', String(30)),
                    Column('io_template', Text()),
                    Column('active', Boolean()))

        model_meta_data.create(self.conn)