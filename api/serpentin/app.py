from flask import Flask
from flask_cors import CORS
from pony.flask import Pony
from serpentin.api import register_api
from serpentin.core.database import connect_to_database


def create_app():
    app = Flask("serpentin")
    app.config["ENV"] = "development"

    # CORS
    CORS(app, origins=["*"])

    # Pony
    Pony(app)

    # API
    register_api(app)

    # Database
    connect_to_database()

    return app
