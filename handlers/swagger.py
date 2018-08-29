def handler(event, context):
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