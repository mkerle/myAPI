import requests
import json

r = requests.post('https://127.0.0.1:8443/auth/login/', json={'username': 'mitch', 'password' : 'Password1'}, verify=False)
print(r.text)

loginData = json.loads(r.text)

token = 'Bearer %s' % (loginData['token'])
r = requests.get('https://127.0.0.1:8443/testapp/permtest/', headers={'Authorization' : token}, verify=False)
print(r.text)

# do ldap search
r = requests.post('https://127.0.0.1:8443/ldapmgmt/search/', json={'sAMAccountName': 'mitch'}, headers={'Authorization' : token}, verify=False)
print(r.text)

r = requests.post('https://127.0.0.1:8443/ldapmgmt/search/', json={'sAMAccountName': 'mitch', 'attributes' : ['distinguishedName', 'sAMAccountName', 'memberOf']}, headers={'Authorization' : token}, verify=False)
print(r.text)

# ldap modify
r = requests.post('https://127.0.0.1:8443/ldapmgmt/modify/', json={'dn': 'CN=mitch,CN=Users,DC=mitch,DC=zone', 'changes' : [{'operation' : 'replace', 'modification' : { 'carLicense' : 'Hervey Bay'}}] }, headers={'Authorization' : token}, verify=False)
print(r.text)

# Token Data Serach
r = requests.post('https://127.0.0.1:8443/ldapmgmt/tokensearch/', json={'sAMAccountName': 'mitch'}, headers={'Authorization' : token}, verify=False)
print(r.text)
