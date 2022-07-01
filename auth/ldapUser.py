
from auth.user import AbstractUser

class LDAPUser(AbstractUser):

    # ldapData is expected to as return from python-ldap library
    def __init__(self, ldapData):
        super().__init__()

        self.username = ldapData.get('userPrincipalName')[0].decode('utf-8')
        self.name = ldapData.get('name')[0].decode('utf-8')

        for group in ldapData.get('memberOf', []):
            self.groups.append(group.decode('utf-8'))

        self.is_authenticated = True