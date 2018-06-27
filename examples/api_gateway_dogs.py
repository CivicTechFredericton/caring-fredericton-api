import flask
import boto3
import json
import random
from services.root.resource import RootSchema

import logging
logger = logging.getLogger(__name__)
blueprint = flask.Blueprint('dog', __name__)
dogs = ["Bernese", "German", "Terrier", "Pug", "English Bulldog", "Aussie Shepard"]

@blueprint.route('/dogs', methods=['POST'])
def post_dog(**attributes):
    body = flask.request.data
    body_json = json.loads(body)
    if(body_json['Name']):
        dogs.append(body_json['Name'])
        return body_json['Name'] + ' added to list'
    else:
        return "Please include Name key in JSON body"


@blueprint.route('/dogs/random', methods=['GET'])
def get_random_dog():
    index = random.randint(0,len(dogs))
    return dogs[index]

@blueprint.route('/dogs/<index>', methods=['GET'])
def get_dog(index):
    return dogs[int(index)]
