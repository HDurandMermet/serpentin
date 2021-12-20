from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


def register_api(app):
    import serpentin.api.compensations
    import serpentin.api.deals
    import serpentin.api.statements
    import serpentin.api.executives

    app.register_blueprint(api_bp, url_prefix="/api")

    return api_bp
