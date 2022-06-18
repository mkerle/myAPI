
from middleware import AbstractMiddleware

from auth.user import JWTUser

class JWTMiddleware(AbstractMiddleware):

    def processRequest(cls, request):

        request['JWT'] = ''

        if (not 'USER' in request):
            request['USER'] = None
            
        if 'HTTP_AUTHORIZATION' in request:
            if ('Bearer' in request['HTTP_AUTHORIZATION']):
                request['JWT'] = request['HTTP_AUTHORIZATION'].replace('Bearer ', '')
                request['USER'] = JWTUser(request['JWT'])

