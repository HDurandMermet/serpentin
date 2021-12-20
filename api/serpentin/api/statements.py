from flask import request
from flask_restful import Resource
from serpentin.api import api
from serpentin.managers.compensations import post_compensation
from serpentin.managers.statements import (
    get_statement_compensations,
    get_statements,
    post_statement,
    post_statement_compensation,
)


class Statements(Resource):
    def get(self):
        """Return statements"""
        statements = get_statements()
        formatted_statements = [s.get_formatted_data() for s in statements]

        return {"statements": formatted_statements}

    def post(self):
        json_data = request.get_json(force=True)
        executive_id = int(json_data['executive'])
        month = int(json_data['month'])
        year = int(json_data['year'])
        response = post_statement(executive_id, month, year)
        return response


api.add_resource(Statements, "/statements")


class StatementCompensations(Resource):
    def get(self):
        """Return statements compensations"""
        statement_compensations = get_statement_compensations()
        formatted_statement_compensations = [
            sc.get_formatted_data() for sc in statement_compensations
        ]

        return {"statement_compensations": formatted_statement_compensations}

    def post(self):
        json_data = request.get_json(force=True)
        compensation = post_compensation(
            json_data['compensation']['name'],
            json_data['compensation']['type']
        )
        statement = post_statement(
            json_data['statement']['executive'],
            json_data['statement']['month'],
            json_data['statement']['year']
        )
        response = post_statement_compensation(
            compensation,
            statement
        )

        return response.get_formatted_data()


api.add_resource(
    StatementCompensations, 
    "/statement_compensations"
)