from flask import request
from flask_restful import Resource
from serpentin.api import api
from serpentin.managers.compensations import (
    post_compensation,
    get_compensations
)


class Compensations(Resource):
    def get(self):
        compensations = get_compensations()
        formatted_compensations = [
            c.get_formatted_data() for c in compensations
        ]
        return {"compensations": formatted_compensations}

    def post(self):
        json_data = request.get_json(force=True)
        name = json_data['name']
        type = json_data['type']
        response = post_compensation(name, type)
        return response.toJSON()


api.add_resource(Compensations, "/compensations")