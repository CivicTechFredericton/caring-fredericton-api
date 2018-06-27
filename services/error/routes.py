import flask
from core import errors
from services.error.resource import ERROR_SCHEMA

import logging
logger = logging.getLogger(__name__)
blueprint = flask.Blueprint('errors', __name__)


@blueprint.app_errorhandler(errors.HttpError)
def handle_error(error):
    return flask.jsonify(ERROR_SCHEMA.dump(error).data), error.status_code


@blueprint.app_errorhandler(errors.UNPROCESSABLE_ENTITY)
def handle_validation_error(error):
    return flask.jsonify(error.data), errors.UNPROCESSABLE_ENTITY
