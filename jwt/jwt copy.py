

import json
import datetime
from authlib.jose import JsonWebToken, JWTClaims
from cryptography.hazmat.primitives import serialization

# class JWTAuthenticationMiddleware(MiddlewareMixin):

#     def process_request(self, request):

#         if ('Authorization' in request.headers):
#             if ('Bearer' in request.headers['Authorization']):
#                 request.user = self._getUserFromJWT(request.headers['Authorization'].replace('Bearer ', ''))

#     def _getUserFromJWT(self, jwt):
        
#         decodedJWT = JWTHelper.decodeJWT(jwt)

#         user = get_user_model()()
#         user.setLDAPGroups(decodedJWT['groups'])
#         user.setJWT(decodedJWT)

#         return user


class JWTHelper():

    JWT_ISSUER = 'jwt.mitch.zone'
    JWT_DEFAULT_EXPIRY = 60     # seconds
    JWT_PRIVATE_KEY_PATH = 'testapp/key.pem'
    JWT_PRIVATE_KEY_PASSWORD = 'Password1'      # retrieve from keyring or at least obfuscate
    JWT_PUBLIC_KEY_PATH = 'testapp/publickey.pem'

    @classmethod
    def getPublicKey(cls):

        pubKey = cls.getJWTPublicKey(cls.JWT_PUBLIC_KEY_PATH).public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        return pubKey

    @classmethod
    def getJWTPublicKey(cls, jwtPublicKeyPath):
        with open(jwtPublicKeyPath, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        return public_key

    @classmethod
    def generateJWTExpiryTime(cls, tokenExpirySecs):

        return int((datetime.datetime.now()+datetime.timedelta(seconds=tokenExpirySecs)).timestamp())

    @classmethod
    def getJWTPrivateKey(cls, jwtPrivateKeyPath, jwtPrivateKeyPassword):
        with open(jwtPrivateKeyPath, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=bytes(jwtPrivateKeyPassword, 'utf-8'),
            )

        return private_key

    @classmethod
    def generateUserJWT(cls, userLDAPData):

        groups = []
        for group in userLDAPData.get('memberOf', []):
            groups.append(group.decode('utf-8'))

        principalName = userLDAPData.get('userPrincipalName')[0].decode('utf-8')
        name = userLDAPData.get('name')[0].decode('utf-8')

        exp = cls.generateJWTExpiryTime(cls.JWT_DEFAULT_EXPIRY)
        payload = {
            'iss': cls.JWT_ISSUER, 
            'sub': principalName, 
            'exp' : exp, 
            'name' : name, 
            'groups' : groups  
        }
        header = {'alg': 'RS256'}

        jwt = JsonWebToken()
        s = jwt.encode(header, payload, cls.getJWTPrivateKey(cls.JWT_PRIVATE_KEY_PATH, cls.JWT_PRIVATE_KEY_PASSWORD))

        return s.decode('utf-8')

    @classmethod
    def validateUserJWT(cls, token):

        try:
            claims_options = { 'iss' : { 'essential' : True, 'values' : [cls.JWT_ISSUER]}, 'exp' : { 'essential' : True, 'validate' : cls.jwtExpired }}

            jwt = JsonWebToken()
            claims = jwt.decode(token, cls.getJWTPrivateKey(cls.JWT_PRIVATE_KEY_PATH, cls.JWT_PRIVATE_KEY_PASSWORD), claims_cls=JWTClaims, claims_options=claims_options)

            return claims.validate()
        except:
            return False

    def jwtExpired(exp):

        try:
            return (int(datetime.datetime.now().timestamp()) > datetime.datetime.fromtimestamp(exp))
        except:
            return False

    @classmethod
    def decodeJWT(cls, token):

        jwt = JsonWebToken()
        return jwt.decode(token, cls.getJWTPrivateKey(cls.JWT_PRIVATE_KEY_PATH, cls.JWT_PRIVATE_KEY_PASSWORD))