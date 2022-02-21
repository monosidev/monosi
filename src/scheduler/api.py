from flask_restful import Api

import scheduler.handlers as handlers

class MsiSchedulerApi(Api):
    VERSION = 'v1'
    PREFIX = f'{VERSION}/api'

    def __init__(self, app):
        super().__init__(app)
        handlers.init_api(self)

def init_api(app):
    return MsiSchedulerApi(app)
