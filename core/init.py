import importlib

import flask
import flask_cors

from core import configuration, db

import logging
from logging import config as logging_config
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logging.getLogger(__name__).setLevel(logging.INFO)

SETTINGS = 'settings'
LOGGING = 'logging'
MODELS = 'models'
APP = 'app'

# Full init sequence. Order matters.
FULL_STAGES_LIST = (SETTINGS, APP, LOGGING, MODELS)

# Set the list of service names which expose API endpoints
SERVICE_NAMES = ['error', 'root', 'dogs', 'todo']

stages_done = {}
app = None


def init_logging():
    root_logger = logging.getLogger()
    root_logger.handlers = []
    logging_config.dictConfig(configuration.get_setting('logging'))
    logger.info('Configured logging')


def init_models():
    service_name = configuration.get_setting('SERVICE_NAME')
    stage = configuration.get_setting('STAGE')
    host = configuration.get_setting('dynamo_host')

    db.init_models(service_name, stage, host)


def init_app():
    global app
    app = flask.Flask(__name__)
    # Add 'Access-Control-Allow-Origin' header to every response
    flask_cors.CORS(app)

    # Scan for any registered blueprints
    for name in SERVICE_NAMES:
        service = importlib.import_module("services.%s.routes" % name)
        app.register_blueprint(service.blueprint)


INIT_STAGES = {
    SETTINGS: configuration.init_settings,
    LOGGING: init_logging,
    MODELS: init_models,
    APP: init_app,
}


def init_application(required_stages=FULL_STAGES_LIST):
    for stage in required_stages:
        if stage not in stages_done:
            logger.info("Starting stage '%s'", stage)
            curr_function = INIT_STAGES[stage]
            curr_function()
            stages_done[stage] = True
            logger.info("Finished stage '%s'", stage)

    return app
