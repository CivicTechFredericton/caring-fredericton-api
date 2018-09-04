from flask import jsonify, Blueprint
from webargs.flaskparser import use_kwargs
from .resource import user_schema

blueprint = Blueprint('users', __name__)


@blueprint.route('/users', methods=["POST"])
@use_kwargs(user_schema, locations=('json',))
def profile_update(**kwargs):
    return jsonify({
        "username": kwargs["username"],
        "password": kwargs["password"],
        "first_name": kwargs["first_name"],
        "last_name": kwargs["last_name"]
    })
