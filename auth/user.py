
class AbstractUser():

    def __init__(self):
        self.is_authenticated = False
        self.groups = []
        self.username = ''
        self.name = ''

    def isAuthenticated(self):
        return self.is_authenticated
        