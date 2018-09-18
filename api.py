import flask
from core import init, errors

app = init.init_application()


# Return validation errors from webargs as JSON
@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, "exc")
    if exc:
        # Get validations from the ValidationError object
        messages = exc.messages
    else:
        messages = ["Invalid request"]
    return flask.jsonify({"messages": messages}), 422


# Handle ResourceValidationError messages
@app.errorhandler(errors.ResourceValidationError)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
