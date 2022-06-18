import requests
import json

r = requests.post('https://127.0.0.1:8443/auth/login/', json={'username': 'mitch', 'password' : 'Password1'}, verify=False)
print(r.text)

loginData = json.loads(r.text)

token = 'Bearer %s' % (loginData['token'])
r = requests.get('https://127.0.0.1:8443/testapp/permtest/', headers={'Authorization' : token}, verify=False)
print(r.text)