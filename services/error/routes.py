from flask import jsonify, Blueprint
from core import errors
from services.error.resource import ERROR_SCHEMA

blueprint = Blueprint('errors', __name__)


@blueprint.app_errorhandler(errors.HttpError)
def handle_error(error):
    return jsonify(ERROR_SCHEMA.dump(error).data), error.status_code


@blueprint.app_errorhandler(errors.ResourceValidationError)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.UNPROCESSABLE_ENTITY)
def handle_validation_error(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'messages': messages}), error.code, headers
    else:
        return jsonify({'messages': messages}), error.code

