from http.client import INTERNAL_SERVER_ERROR, BAD_REQUEST, NOT_FOUND, UNPROCESSABLE_ENTITY
from werkzeug import exceptions


class HttpError(Exception):
    status_code = INTERNAL_SERVER_ERROR
    code = 'error.internal_sever_error'
    message = 'Internal server error'

    def __init__(self, code=None, message=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code

        if code is not None:
            self.code = code

        if message is not None:
            self.message = message

        super().__init__(self.message)


class ResourceNotFoundError(HttpError):
    status_code = NOT_FOUND
    message = 'Resource not found error'


class ResourceReadonly(HttpError):
    status_code = BAD_REQUEST
    message = 'Resource is read-only'


class ResourceValidationError(exceptions.UnprocessableEntity):
    status_code = UNPROCESSABLE_ENTITY

    def __init__(self, messages):
        self.data = {'messages': messages}
        super().__init__()

    def to_dict(self):
        return self.data


class CognitoError(HttpError):
    code = 'error.cognito.error'
    message = 'Cognito error'


class SESError(HttpError):
    code = 'error.ses.error'
    message = 'SES error'


class S3Error(HttpError):
    code = 'error.s3.error'
    message = 'S3 error'
