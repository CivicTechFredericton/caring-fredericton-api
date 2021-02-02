from flask import jsonify, Blueprint
from caringapp.core import errors
from caringapp.endpoints.error.schemas import ERROR_SCHEMA

blueprint = Blueprint('errors', __name__)


@blueprint.app_errorhandler(errors.HttpError)
def handle_error(error):
    return jsonify(ERROR_SCHEMA.dump(error).data), error.status_code


@blueprint.app_errorhandler(errors.ResourceConflictError)
def handle_resource_conflict_error(error):
    return jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.BadRequestError)
def handle_bad_request_error(error):
    return jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.ResourceValidationError)
def handle_resource_validation_error(error):
    return jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.ResourceNotFoundError)
def handle_resource_not_found_error(error):
    return jsonify(error.to_dict()), error.status_code


@blueprint.app_errorhandler(errors.DEFAULT_ERROR)
def handle_validation_error(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'messages': messages}), error.code, headers
    else:
        return jsonify({'messages': messages}), error.code

