from flask_restful import Api, Resource

from . import main

main_api = Api(main)


class MainResource(Resource):
    def get(self):
        pass

    def post(self):
        pass


main_api.add_resource(MainResource, '/')
