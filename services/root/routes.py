import flask
from services.root.resource import RootSchema

import logging
logger = logging.getLogger(__name__)
blueprint = flask.Blueprint('root', __name__)


@blueprint.route('/')
def root():
    schema = RootSchema(flask.current_app)
    return flask.jsonify(schema.dump({}).data)


@blueprint.route('/hello')
def hello():
    return 'Hello World'
