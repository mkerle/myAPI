
from helpers import httpHelper



def isAuthenticated(func):

    def isAuthenticatedWrapper(self, request, start_response):
        user = request.get('USER', None)
        if (user and user.isAuthenticated()):
            return func(self, request, start_response)
        else:
            return httpHelper.send401Response(request, start_response)

    return isAuthenticatedWrapper

def hasPermission(group):

    def checkPermission(func):

        def checkPermissionWrapper(self, request, start_response):
            user = request.get('USER', None)
            if (user and group in user.groups):
                return func(self, request, start_response)
            else:
                return httpHelper.send401Response(request, start_response)

        return checkPermissionWrapper

    return checkPermission

def allowedHTTPMethods(methods=['OPTIONS']):

    def checkMethods(func):

        def checkMethodsWrapper(self, request, start_response):
            if (request['REQUEST_METHOD'] in methods):
                if (request['REQUEST_METHOD'] == 'OPTIONS'):
                    allowedMethods = str(methods).strip("'[]").replace("'", '')
                    # for meth in methods:
                    #     allowedMethods += ' %s' % (meth)
                    # allowedMethods.lstrip().replace(' ', ', ')

                    headers = [
                        ('Content-type', 'application/json; charset=utf-8'), 
                        ('Access-Control-Allow-Origin', request['HTTP_ORIGIN']), 
                        #('Access-Control-Allow-Credentials', 'true'), 
                        ('Access-Control-Allow-Headers', '%s, Content-Type' % (request['HTTP_ACCESS_CONTROL_REQUEST_HEADERS'])), 
                        ('Access-Control-Allow-Methods', allowedMethods), 
                        ('Access-Control-Max-Age', '5')
                        ]
                    start_response('204 No Content', headers)
                    return [b'']
                else:
                    return func(self, request, start_response)

            return httpHelper.send400Response(request, start_response)

        return checkMethodsWrapper

    return checkMethods
