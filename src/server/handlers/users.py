import logging
from flask_restful import abort, request
from sqlalchemy.exc import IntegrityError

from server.models import User

from .base import BaseResource


class UserResource(BaseResource):
    @property
    def resource(self):
        return User

    @property
    def key(self):
        return "user"

    def get(self):
        obj = User.create_or_load()

        return {self.key: obj.to_dict()}

    def post(self):
        req = request.get_json(force=True)
        
        try:
            obj = User.update(req)
        except IntegrityError as e:
            logging.error(e)
            abort(422)
        except Exception as e:
            logging.error(e)
            abort(500)

        return {self.key: obj.to_dict()}, 200
