import abc
import logging
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from server.middleware.db import db

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
        obj_list = self._all()

        return {self.key: obj_list}

    def post(self):
        req = request.get_json(force=True)
        self._validate(req)
        
        try:
            obj = self.resource.from_dict(req)

            self._create(obj)
            self._after_create(obj)
        except IntegrityError as e:
            logging.error(e)
            abort(422)
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}, 200

    def _create(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except IntegrityError:
            raise
        except Exception as e:
            raise Exception("DB: Couldn't persist record")

    def _after_create(self, sqlalc_obj):
        pass

    def _all(self):
        try:
            objs = db.session.query(self.resource).all()
        except:
            abort(500)
        return [obj.to_dict() for obj in objs]


class CrudResource(BaseResource):
    def _retrieve_by_id(self, object_id):
        try:
            obj = db.session.query(self.resource).filter(self.resource.id == object_id).one()
        except:
            abort(404)
        return obj

    def _validate(self, req):
        pass
        # return self.resource.validate(req)

    def get(self, **kwargs):
        obj_id = kwargs['obj_id']
        obj = self._retrieve_by_id(obj_id)

        return {self.key: obj.to_dict()}

    def put(self, obj_id):
        request.args.get('obj_id')
        obj = self._retrieve_by_id(obj_id)

        req = request.get_json(force=True)
        self._validate(req)
        
        try:
            self._update(obj, req)
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}
    
    def delete(self, obj_id):
        request.args.get('obj_id')
        obj = self._retrieve_by_id(obj_id)

        try:
            self._delete(obj)
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}


    def _update(self, obj, updates):
        try:
            for k, v in updates.items():
                setattr(obj, k, v)

            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            raise Exception("DB: Couldn't update record")

    def _delete(self, obj):
        try:
            db.session.delete(obj)
            db.session.commit()
            self._after_destroy(obj)
        except:
            raise Exception("DB: Couldn't delete record")

    def _after_destroy(self, sqlalc_obj):
        pass
