import json

def getHTTPRequestBody(request):

    request_body_size = 0
    try:
        request_body_size = int(request.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    return request['wsgi.input'].read(request_body_size)

def getJSONRequestBody(request):

    request_body = getHTTPRequestBody(request)
    return json.loads(request_body.decode('utf-8'))


def sendJSONResponse(start_response, jsonResponse, status='200 OK', headers=None):

    if (headers is None):
        headers = [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', 'http://127.0.0.1:4200'), ('Access-Control-Allow-Credentials', 'true')]
    else:
        foundContentType = False
        for header in headers:
            if 'Content-type' in header[0]:
                foundContentType = True

        if (not foundContentType):
            headers.append(('Content-type', 'application/json; charset=utf-8'))

    start_response(status, headers)
    return [bytes(json.dumps(jsonResponse), 'utf-8')]

###############################################################################
# Generic Bad Responsees
###############################################################################

def send404Response(request, start_response):

    status = '404 Not Found'
    start_response(status, [])
    return [b'']

def defaultSend401Response(request, start_response):

    status = '401 Unauthorized'
    start_response(status, [])
    return [b'']

def send400Response(request, start_response):

    status = '400 Bad Request'
    start_response(status, [])
    return [b'']   

send401Response = defaultSend401Response