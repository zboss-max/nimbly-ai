"""
main路由
"""
from flask_restful import Api, Resource

from . import main_bp

main_api = Api(main_bp)


class IndexResource(Resource):
    def get(self):
        pass

    def post(self):
        pass


main_api.add_resource(IndexResource, '/')
