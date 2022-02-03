from flask_restful import Api

import server.handlers as handlers

class MsiApi(Api):
    VERSION = 'v1'
    PREFIX = f'{VERSION}/api'

    def __init__(self, app):
        super().__init__(app)
        handlers.init_api(self)
