from wsgiref.simple_server import make_server
import json
import ssl
import hashlib
import secrets
import base64
import re

from router.router import HTTPRoute, HTTPRouter
from auth import LDAPAuthentication
from testapp.testapp import testApp

from middleware.jwtMiddleware import JWTMiddleware

SERVER_HTTP_PORT = 8443
SERVER_CERT_FILE = 'cert.pem'
SERVER_KEY_FILE = 'key.pem'

router = HTTPRouter()
router.addRoute(HTTPRoute('/testapp/', testApp()))
router.addRoute(HTTPRoute('/auth/', LDAPAuthentication()))

middleware = [JWTMiddleware()]


def main_router(environ, start_response):

    for m in middleware:
        m.processRequest(environ)
    #print(environ)

    return router.processRequest(environ, start_response)


def doSSL(sock, certfile, keyfile, ca_certs=None):
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=None, capath=None, cadata=None)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    return context.wrap_socket(sock, server_side=True, do_handshake_on_connect=True)
                                           

with make_server('', SERVER_HTTP_PORT, main_router) as httpd:
    print("Serving HTTP on port %d..." % (SERVER_HTTP_PORT))
    
    httpd.socket = doSSL(httpd.socket, SERVER_CERT_FILE, SERVER_KEY_FILE, ca_certs=None)
    
    # Respond to requests until process is killed
    httpd.serve_forever()