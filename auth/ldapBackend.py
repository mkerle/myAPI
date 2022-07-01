import ldap

from auth.ldapUser import LDAPUser

class LDAPBackend():

    LDAP_SERVER_IP = '10.1.1.254'
    LDAP_SERVER_PORT = '389'
    LDAP_BASE_DN = 'cn=users,dc=mitch,dc=zone'
    LDAP_BIND_DN = 'svc_ldap_bind_acc'
    LDAP_BIND_PASSWORD = 'Password1'
    LDAP_TLS_ENABLE = False

    def authenticate(self, username=None, password=None):

        if (username is not None or password is not None):

            ldapResult = self.ldapSearchUser(username, password)
            if (self.ldapAuthenticate(ldapResult)):
                
                return LDAPUser(ldapResult[0][1])

        return None

    def ldapSearchUser(self, user, password):

        try:
            constr = 'ldap://' + self.LDAP_SERVER_IP + ':' + self.LDAP_SERVER_PORT
            if (self.LDAP_TLS_ENABLE):
                constr = 'ldaps://' + self.LDAP_SERVER_IP + ':' + self.LDAP_SERVER_PORT

            con = ldap.initialize(constr, bytes_mode=False)

            if (self.LDAP_TLS_ENABLE):
                con.set_option(ldap.OPT_X_TLS_CACERTFILE, self.LDAP_TLS_CERT_PATH)
                con.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
                con.start_tls_s()

            con.simple_bind_s(self.LDAP_BIND_DN, self.LDAP_BIND_PASSWORD)

            userLDAPData = con.search_s(self.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, u'(sAMAccountName=' + user + ')')
            con.unbind_s()

            # bind using user DN and password - if wrong will throw exception
            userDN = self.getUserDN(userLDAPData)
            con = ldap.initialize(constr, bytes_mode=False)
            con.simple_bind_s(userDN, password)

            return userLDAPData
        except:
            return None

    def ldapAuthenticate(self, ldapSearchResult):

        if (ldapSearchResult is not None):
            if (len(ldapSearchResult) == 1):
                if (ldapSearchResult[0][1]):
                    return True

        return False

    def getUserDN(self, userData):

        dn = ''
        if (userData and len(userData) == 1 and userData[0][1] and 'distinguishedName' in userData[0][1]):
            return userData[0][1]['distinguishedName'][0].decode('utf-8')

        return dn