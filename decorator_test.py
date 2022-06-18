
class myClass():

    def classFunc(self, val1, val2):
        print(val1*val2)


my = myClass()
my.classFunc(2,3)


def my_decorator(func):

    def wrapper(self, val1, val2):
        func(self, val1*val1, val2*val2)

    return wrapper



class myClass2():

    @my_decorator
    def classFunc(self, val1, val2):
        print(val1*val2)

my2 = myClass2()
my2.classFunc(2,3)


class myMath():

    def square(self, x):
        return x*x

my3 = myMath()
print(my3.square(3))

def square_decorator(func):

    def wrapper(self, x):
        return func(self,x*x)

    return wrapper

class myMath2():

    @square_decorator
    @square_decorator
    def square(self, x):
        return x*x

my4 = myMath2()
print(my4.square(2))


def text_decorator(specialText):
    def appender(func):
        def wrapper(self, t):
            return func(self, t + ' plus a bit extra %s' % (specialText))

        return wrapper

    return appender

class textClass():

    @text_decorator('some extra for free')
    def append(self, t):
        return 'This is the original return + %s' % (t)


t = textClass()
print(t.append('my appended text'))
