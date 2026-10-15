"""
signin路由
"""
from flask_restful import Api, Resource

from .. import auth_bp

auth_api = Api(auth_bp)


class SignInResource(Resource):
    def get(self):
        pass

    def post(self):
        pass


auth_api.add_resource(SignInResource, '/signin')