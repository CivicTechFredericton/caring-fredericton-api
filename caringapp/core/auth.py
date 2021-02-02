import boto3
import flask


def get_current_user_id() -> str:
    """
    Returns the Id of the currently executing user (if present)

    If no user is logged in; returns lambda user id from boto3 identity
    """
    # Check for flask identity to use instead of lambda user id
    if not flask.has_request_context() or 'identity' not in flask.g or flask.g.identity is None:
        # Return lambda user id
        client = boto3.client('sts')
        return client.get_caller_identity()['UserId']

    # Return flask user identity
    return flask.g.identity.id if flask.g.identity.id else 'local-user'
