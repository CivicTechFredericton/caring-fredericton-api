from http import HTTPStatus


class HttpError(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
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


class BadRequestError(HttpError):
    status_code = HTTPStatus.BAD_REQUEST.value

    def __init__(self, messages):
        self.data = {'messages': messages}
        super().__init__()

    def to_dict(self):
        return self.data


class ResourceConflictError(HttpError):
    status_code = HTTPStatus.CONFLICT.value

    def __init__(self, messages):
        self.data = {'messages': messages}
        super().__init__()

    def to_dict(self):
        return self.data


class ResourceNotFoundError(HttpError):
    status_code = HTTPStatus.NOT_FOUND.value

    def __init__(self, messages):
        self.data = {'messages': messages}
        super().__init__()

    def to_dict(self):
        return self.data


class ResourceValidationError(HttpError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value

    def __init__(self, messages):
        self.data = {'messages': messages}
        super().__init__()

    def to_dict(self):
        return self.data


class SESError(HttpError):
    code = 'error.ses.error'
    message = 'SES error'


class S3Error(HttpError):
    code = 'error.s3.error'
    message = 'S3 error'
