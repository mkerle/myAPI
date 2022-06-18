
from jwt.jwt import JWTHelper

class AbstractUser():

    def __init__(self):
        self.is_authenticated = False
        self.groups = []
        self.username = ''
        self.name = ''

    def isAuthenticated(self):
        return self.is_authenticated

class LDAPUser(AbstractUser):

    def __init__(self, ldapData):
        super().__init__()

        self.username = ldapData.get('userPrincipalName')[0].decode('utf-8')
        self.name = ldapData.get('name')[0].decode('utf-8')

        for group in ldapData.get('memberOf', []):
            self.groups.append(group.decode('utf-8'))

        self.is_authenticated = True

class JWTUser(AbstractUser):

    def __init__(self, token):
        super().__init__()

        try:
            if (JWTHelper.validateUserJWT(token)):
                decodedJWT = JWTHelper.decodeJWT(token)

                self.username = decodedJWT.get('sub', '')
                self.name = decodedJWT.get('name', '')
                self.groups = decodedJWT.get('groups', [])

                self.tokenExpiry = decodedJWT.get('exp', 0)

                # if validation was successful then user is authenticated
                self.is_authenticated = True

        except Exception as e:
            print(e)


