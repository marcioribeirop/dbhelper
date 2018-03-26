from dbhelper.base import Session
from dbhelper.utils.entities import Model, App, Client, ModelMetaData, Product
from dbhelper.utils.keras_fix import make_keras_picklable
from sqlalchemy.orm.exc import NoResultFound
import pickle


class HelperRuntime(object):

    def save(self, **kwargs):  # model, io_template, client, version, app, product, active, model_name

        session = Session()

        self.validate(kwargs)

        model, io_template = self.serialize(kwargs)

        app_query = session.query(App).filter(App.name == kwargs.pop("app")).first()

        if 'client' in kwargs:
            client = session.query(Client).filter(Client.name == kwargs.pop("client")).first().id

        else:
            client = None

        if 'product' in kwargs:
            product = session.query(Product).filter(Product.name == kwargs.pop("product")).first().id

        else:
            product = None

        model_new = Model(model_source=model)

        session.add(model_new)

        session.flush()

        model_meta_data_new = ModelMetaData(model_id=model_new.id, io_template=io_template,
                                            client_id=client, version=kwargs.pop("version"),
                                            app_id=app_query.id, product_id=product,
                                            active=kwargs.pop("active"), model_name=kwargs.pop("model_name"))

        session.add(model_meta_data_new)

        session.commit()
        session.close()

    def load(self, app, model_name, version, client=None, product=None):

        session = Session()

        model_meta_data_query = self.query_model_meta_data(session, app, model_name, version, client, product)

        model_query = session.query(Model).filter(Model.id == model_meta_data_query.model_id).first()

        model, io_template = self.deserialize(model_query.model_source,
                                              io_template_serialized=model_meta_data_query.io_template)

        session.close()

        return model, io_template

    def serialize(self, kwargs):
        model = self.serialize_model(kwargs.pop('model'))
        io_template = pickle.dumps(kwargs.pop('io_template'))

        return model, io_template

    @staticmethod
    def serialize_model(model):
        try:

            make_keras_picklable() # Fix the Keras bug for proper pickling

            serialized_model = pickle.dumps(model)
            return serialized_model
        except:
            raise RuntimeError("Could not save properly the passed model.")

    def deserialize(self, model_serialized, io_template_serialized):
        model = self.deserialize_model(model_serialized)

        io_template = pickle.loads(io_template_serialized)
        return model, io_template

    @staticmethod
    def deserialize_model(model):
        try:
            make_keras_picklable()

            deserialized_model = pickle.loads(model)

            return deserialized_model
        except:
            raise RuntimeError("Could not load properly the requested model.")

    @staticmethod
    def validate(kwargs):
        check_fields = {"model", "io_template", "version", "active", "app"}
        if set(kwargs.keys()).intersection(check_fields) != check_fields:
            raise IOError("The argument(s) %s need to be passed in order to save a model.".format(
                *(check_fields - set(kwargs.keys()))))

    @staticmethod
    def query_model_meta_data(session, app, model_name, version, client=None, product=None):

        if client == None:
            model_meta_data_query = session.query(ModelMetaData).filter(ModelMetaData.model_name == model_name). \
                filter(ModelMetaData.app.has(App.name == app)).filter(ModelMetaData.version == version). \
                filter(ModelMetaData.client == client). \
                filter(ModelMetaData.product == product).first()

        elif product == None:
            model_meta_data_query = session.query(ModelMetaData).filter(ModelMetaData.model_name == model_name). \
                filter(ModelMetaData.app.has(App.name == app)).filter(ModelMetaData.version == version). \
                filter(ModelMetaData.client.has(Client.name == client)). \
                filter(ModelMetaData.product == product).first()
        else:
            model_meta_data_query = session.query(ModelMetaData).filter(ModelMetaData.model_name == model_name).\
                filter(ModelMetaData.app.has(App.name == app)).filter(ModelMetaData.version == version).\
                filter(ModelMetaData.client.has(Client.name == client)).\
                filter(ModelMetaData.product.has(Product.name == product)).first()

        if model_meta_data_query is None:
            raise NoResultFound("Requested model could not be found.")

        return model_meta_data_query
