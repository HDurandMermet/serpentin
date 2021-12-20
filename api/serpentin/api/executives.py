from flask_restful import Resource
from serpentin.api import api
from serpentin.managers.executives import get_executives


class Executives(Resource):
    def get(self):
        """Return executives"""
        executives = get_executives()
        formatted_executives = [e.get_formatted_data() for e in executives]
        return {"executives": formatted_executives}


api.add_resource(Executives, "/executives")