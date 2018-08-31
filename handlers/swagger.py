def handler(event, context):
    """
    Handler event to show the Swagger documentation for the APIs
    :param event: The object containing the request details (query strings, body, etc.)
    :param context: The object containing runtime information (request ID, CloudWatch log group, etc.)
    :return: The contents of the Swagger file
    """
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html',
        }
    }

    if event['path'] == '/':
        path = '/index.html'
    else:
        path = event['path']

    with open('apidocs%s' % path) as file:
        response['body'] = str(file.read())

    return response
