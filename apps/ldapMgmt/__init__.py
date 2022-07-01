import ldap
from router.router import HTTPRoute, HTTPRouter
from helpers import httpHelper
from helpers.decorators import isAuthenticated, hasPermission, allowedHTTPMethods

class LDAPMgmtApp(HTTPRouter):

    LDAP_SERVER_IP = '10.1.1.254'
    LDAP_SERVER_PORT = '389'
    LDAP_BASE_DN = 'cn=users,dc=mitch,dc=zone'
    LDAP_BIND_DN = 'svc_ldap_bind_acc'
    LDAP_BIND_PASSWORD = 'Password1'
    LDAP_TLS_ENABLE = False

    def __init__(self):
        super().__init__()

    def addInitRoutes(self):
        
        self.addRoute(HTTPRoute('search/', self.search))
        self.addRoute(HTTPRoute('modify/', self.modify))
        self.addRoute(HTTPRoute('tokensearch/', self.getTokenData))
        


    @allowedHTTPMethods(['OPTIONS', 'POST'])
    @isAuthenticated
    @hasPermission('CN=DUMMY_GROUP,CN=Users,DC=mitch,DC=zone')
    def getTokenData(self, request, start_response):

        reqData = httpHelper.getJSONRequestBody(request)

        filter = u'(sAMAccountName=' + reqData['sAMAccountName'] + ')'
        attrlist = ['cn', 'distinguishedName', 'displayName', 'sAMAccountName', 'mail',
                        'labTokenUser', 'labTokenStartDate', 'labTokenGenericAttribute',
                        'labTokenEnabled1', 'labTokenGenericAttribute1', 'labTokenEnrolled1', 'labTokenSerial1',
                        'labTokenEnabled2', 'labTokenGenericAttribute2', 'labTokenEnrolled2', 'labTokenSerial2',
                        'labTokenEnabled3', 'labTokenGenericAttribute3', 'labTokenEnrolled3', 'labTokenSerial3']
        
        results = self._ldapSearch(filter, attrlist)

        if (results):
            return httpHelper.sendJSONResponse(start_response, self._parseLDAPData(results))
        else:
            return httpHelper.sendJSONResponse(start_response, {})


    @allowedHTTPMethods(['OPTIONS', 'POST'])
    @isAuthenticated
    @hasPermission('CN=DUMMY_GROUP,CN=Users,DC=mitch,DC=zone')
    def search(self, request, start_response):

        print('Running search...')

        reqData = httpHelper.getJSONRequestBody(request)

        filter = u'(sAMAccountName=' + reqData['sAMAccountName'] + ')'
        attrlist = reqData.get('attributes', None)

        results = self._ldapSearch(filter, attrlist)

        if (results):
            return httpHelper.sendJSONResponse(start_response, self._parseLDAPData(results))
        else:
            return httpHelper.sendJSONResponse(start_response, {})

    @allowedHTTPMethods(['OPTIONS', 'POST'])
    @isAuthenticated
    @hasPermission('CN=DUMMY_GROUP,CN=Users,DC=mitch,DC=zone')
    def modify(self, request, start_response):

        reqData = httpHelper.getJSONRequestBody(request)

        dn = reqData['dn']
        modList = self._prepareModifyList(reqData['changes'])

        if (self._ldapModify(dn, modList)):
            return httpHelper.sendJSONResponse(start_response, { 'result' : 'OK' } )
        else:
            return httpHelper.sendJSONResponse(start_response, { 'result' : 'failed' } )

    def _prepareModifyList(self, mods):

        modList = []
        for mod in mods:
            ldapOp = None
            if (mod['operation'] == 'add'):
                ldapOp = ldap.MOD_ADD
            elif (mod['operation'] == 'replace'):
                ldapOp = ldap.MOD_REPLACE
            elif (mod['operation'] == 'delete'):
                ldapOp = ldap.MOD_DELETE

            attr = list(mod['modification'].keys())[0]
            modList.append( (ldapOp, attr, bytes(mod['modification'][attr], 'utf-8')) )

        return modList


    def _ldapModify(self, dn, modList):

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

            con.modify_s(dn, modList)

            return True
        except Exception as e:
            print(e)

        return False

    def _parseLDAPData(self, ldapData):

        parsedData = { 'results' : [ ] }

        for user in ldapData:
            parsedUser = {}
            
            for k in user[1]:
                if (k not in ['objectGUID', 'objectSid']):
                    if (type(user[1][k]) == bytes):
                        parsedUser[k] = user[1][k].decode('utf-8')
                    elif (type(user[1][k]) == list):
                        parsedUser[k] = []
                        for val in user[1][k]:
                            if (type(val) == bytes):
                                parsedUser[k].append(val.decode('utf-8'))
                            else:
                                parsedUser[k].append(val)

                        # python-ldap returns a lot of data as a list
                        # to make life easy later change lists of lenth 1 to just the value
                        # NOTE this is making an assumption that may cause other issues!!!!
                        if (len(parsedUser[k]) == 1):
                            parsedUser[k] = parsedUser[k][0]
                    else:
                        parsedUser[k] = user[1][k]

            parsedData['results'].append( parsedUser )

        return parsedData   


    def _ldapSearch(self, filter, attrlist):

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

            userLDAPData = con.search_s(self.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, filter, attrlist)
            con.unbind_s()

            return userLDAPData
        except:
            return None

