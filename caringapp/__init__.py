from flask import Flask
from flask_cors import CORS

from caringapp import endpoints
from caringapp.core import logging


def create_app():
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    # Setup logging
    logging.init_app()

    # Register the endpoints
    endpoints.init_app(app)

    return app
