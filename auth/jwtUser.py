
from auth.user import AbstractUser
from jwt.jwt import JWTHelper

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