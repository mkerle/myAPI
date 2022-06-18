
from abc import abstractclassmethod


class AbstractMiddleware():

    @abstractclassmethod
    def processRequest(cls, request):
        pass