from dbhelper.base import Base, Session
from dbhelper.utils.entities import Model, App, Client, ModelMetaData
import pickle


class HelperRuntime(object):

    def save(self, **kwargs):  # model, requirements, io_template, client, version, app, product, active

        session = Session()

        self.validate(kwargs)
        model, io_template, requirements = self.serialize(kwargs)

        model_new = Model(model_source=model)

        session.add(model_new)
        session.flush()

        model_meta_data_new = ModelMetaData(model_id=model_new.id, requirements=requirements, io_template=io_template,
                                            client_id=kwargs.get("client_id", None), version=kwargs.pop("version"),
                                            app_id=kwargs.pop("app_id", None), product=kwargs.pop("product", None),
                                            active=kwargs.pop("active"))

        session.add(model_meta_data_new)

        session.commit()
        session.close()

    def load(self, model_id):

        session = Session()

        model_query = session.query(Model).filter(Model.id == model_id).first()
        import pdb;pdb.set_trace()
        model = self.deserialize(model_query.model_source)

        return model

    def serialize(self, kwargs):
        model = str(self.serialize_model(kwargs.pop('model')))
        io_template = pickle.dumps(kwargs.pop('io_template'))
        requirements = pickle.dumps(kwargs.pop('requirements'))

        return model, io_template, requirements

    def serialize_model(self, model):
        try:
            try:
                serialized_model = pickle.dumps(model)
                return serialized_model
            except:
                model = model.to_json()
                serialized_model = pickle.dumps(model)
                return serialized_model
        except:
            raise

    def deserialize(self, model_serialized):
        model = self.deserialize_model(model_serialized)
        return model

    def deserialize_model(self, model):
        try:
            try:
                deserialized_model = pickle.loads(eval(model))
                if type(deserialized_model) == str:
                    raise RuntimeError()
                else:
                    return deserialized_model
            except:
                from keras.models import model_from_json
                model = pickle.loads(eval(model))
                deserialized_model = model_from_json(model)
                return deserialized_model
        except:
            raise

    def validate(self, kwargs):
        check_fields = {"model", "requirements", "io_template", "version", "active"}
        if set(kwargs.keys()).intersection(check_fields) != check_fields:
            raise IOError("The argument(s) %s need to be passed in order to save a model.".format(
                *(check_fields - set(kwargs.keys()))))

    def build_environment(self):
        pass
