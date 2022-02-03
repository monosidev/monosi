import abc
import logging
from flask import request
from flask_restful import Resource, abort

class BaseResource(Resource):
    @abc.abstractproperty
    def key(self):
        raise NotImplementedError
    
    @abc.abstractproperty
    def resource(self):
        raise NotImplementedError

    def _validate(self, req):
        raise NotImplementedError

class ListResource(BaseResource):
    def _validate(self, req):
        pass
        # self.resource.validate(req)

    def get(self):
        obj_list = self.resource.all()
        obj_dict_list = [obj.to_dict() for obj in obj_list]

        return {self.key: obj_dict_list}

    def post(self):
        req = request.get_json(force=True)
        self._validate(req)

        obj = self.resource.from_dict(req)

        try:
            obj.create()
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}, 200

class CrudResource(BaseResource):
    def _retrieve_by_id(self, object_id):
        try:
            obj = self.resource.query.get(object_id)
        except:
            abort(404)
        return obj

    def _validate(self, req):
        pass
        # return self.resource.validate(req)

    def get(self, obj_id):
        obj = self._retrieve_by_id(obj_id)

        return {self.key: obj.to_dict()}

    def put(self, obj_id):
        obj = self._retrieve_by_id(obj_id)

        req = request.get_json(force=True)
        self._validate(req)
        
        try:
            obj.update(req)
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}
    
    def delete(self, obj_id):
        obj = self._retrieve_by_id(obj_id)

        try:
            obj.delete()
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}
