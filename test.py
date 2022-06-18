from router.router import HTTPRoute, HTTPRouter

def printTest(request, start_response):

    print('TEST!!!')

route = HTTPRoute('/test/', printTest)

environ = { }
environ['PATH_INFO'] = '/test/'

route.processRequest(environ, '')


################################################################

router = HTTPRouter()
router.addRoute(route)

router.processRequest(environ, '')


################################################################

class childRouter(HTTPRouter):

    def __init__(self):
        super().__init__()
        self.addRoute(HTTPRoute('login/', self.login))

    def login(self, request, start_response):
        print('LOGGED IN!!!')

router.addRoute(HTTPRoute('/child/', childRouter()))
print('Number of routes: %d' % (len(router.routes)))

router.processRequest({'PATH_INFO' : '/child/login/'}, '')


################################################################

router.addRoute(HTTPRoute('/badtype/', 1))
router.processRequest({'PATH_INFO' : '/badtype/'}, '')
