import re
import hashlib
import secrets

from middleware import AbstractMiddleware
from auth.user import AbstractUser

class DigestAuthMiddleware(AbstractMiddleware):

    def __init__(cls):

        cls.userDB = { 'mitch' : 'Password1', 'dog' : 'Password1', 'turd' : 'P@ssword!' }

        cls.REALM = 'auth.mitch.zone'
        cls.OPAQUE = secrets.token_hex()

        cls.nonceCache = { }

    def processRequest(cls, request):

        if (not 'USER' in request):
            request['USER'] = None
            
        if (request['USER'] is None):
            request['USER'] = cls.authenticate(request)

    def authenticate(cls, request):
        
        if ('HTTP_AUTHORIZATION' in request and 'Digest' in request['HTTP_AUTHORIZATION']):

            username, realm, nc, nonce, cnonce, qop, response = cls._getDigestValues(request['HTTP_AUTHORIZATION'])

            HA1 = str(cls._md5('%s:%s:%s' % (username, realm, cls.passwordLookup(username))))
            HA2 = str(cls._md5('%s:%s' % (request['REQUEST_METHOD'], request['PATH_INFO'])))

            response_calc = str(cls._md5('%s:%s:%s:%s:%s:%s' % (HA1, nonce, nc, cnonce, qop, HA2)))

            if (response == response_calc):
                user = AbstractUser()
                user.is_authenticated = True
                user.username = username

                return user

            else:
                return None

    
    def passwordLookup(cls, username):

        return cls.userDB.get(username, None)


    def send401Response(cls, request, start_response):

        id = request.get('REMOTE_ADDR', '') + request.get('HTTP_USER_AGENT', 'NO-USER-AGENT') + request.get('PATH_INFO', '') + request.get('REQUEST_METHOD', '')

        if (id not in cls.nonceCache):
            cls.nonceCache[id] = secrets.token_hex()

        headers = headers = [('WWW-Authenticate', 'Digest realm="%s",qop="auth",nonce="%s",opaque="%s"' % (cls.REALM, cls.nonceCache[id], cls.OPAQUE))]
        start_response('401 Unauthorized', headers)
        return [b'401 Unauthorized']



    def _getDigestValues(cls, digest):

        username = ''            
        match = re.match(r'.*username="(.*?)",?.*', digest)
        if (match is not None):
            username = match.group(1).replace('"', '')

        realm = ''
        match = re.match(r'.*realm="(.*?)",?.*', digest)
        if (match is not None):
            realm = match.group(1).replace('"', '')

        nc = ''
        match = re.match(r'.*nc=(.*?),.*', digest)
        if (match is not None):
            nc = match.group(1).replace('"', '')

        nonce = ''
        match = re.match(r'.* nonce="(.*?)",?.*', digest)
        if (match is not None):
            nonce = match.group(1).replace('"', '')

        cnonce = ''
        match = re.match(r'.*cnonce="(.*?)",?.*', digest)
        if (match is not None):
            cnonce = match.group(1).replace('"', '')

        qop = ''
        match = re.match(r'.*qop=(.*?),.*', digest)
        if (match is not None):
            qop = match.group(1).replace('"', '')

        response = ''
        match = re.match(r'.*response="(.*?)",?.*', digest)
        if (match is not None):
            response = match.group(1).replace('"', '')

        return username, realm, nc, nonce, cnonce, qop, response

    def _md5(cls, s):

        return hashlib.md5(bytes(s, 'utf-8')).hexdigest()
