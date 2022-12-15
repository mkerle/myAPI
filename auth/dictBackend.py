
from auth.user import AbstractUser

# simple plain text database for users
# test purposes only
class DictionaryBackend():

    def __init__(self):

        self.userDB = {
            'mitch' : { 'username' : 'mitch', 'password' : 'Password1', 'groups' : [] }
        }

    def authenticate(self, username=None, password=None):

        if (username is not None and password is not None):

            if (username in self.userDB) and password == self.userDB[username]['password']:

                user = AbstractUser()
                user.is_authenticated = True
                user.groups = self.userDB[username]['groups']
                user.username = username

                return user


        return None