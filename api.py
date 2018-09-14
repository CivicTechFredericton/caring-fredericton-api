from core import init
import flask
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
