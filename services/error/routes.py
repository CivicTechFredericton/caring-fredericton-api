import flask
from core import errors
from services.error.resource import ERROR_SCHEMA

import logging
logger = logging.getLogger(__name__)
blueprint = flask.Blueprint('errors', __name__)


@blueprint.app_errorhandler(errors.HttpError)
def handle_error(error):
    return flask.jsonify(ERROR_SCHEMA.dump(error).data), error.status_code


@blueprint.app_errorhandler(errors.ResourceValidationError)
def handle_invalid_usage(error):
    return flask.jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.UNPROCESSABLE_ENTITY)
def handle_validation_error(error):
    error.data.pop('schema', None)  # Remove schema from response
    return flask.jsonify(error.data), errors.UNPROCESSABLE_ENTITY

