def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return inner


class CustomException(Exception):
    pass


def subgen():
    message = None
    while True:
        try:
            message = yield
            if message == 2:
                break
        except CustomException:
            break
        else:
            print('send', message)
    return f'Return  from subgen(), message {message}'


@coroutine
def delegator(g):
    result = yield from g   # pep380
    return result


# 1 вариант:
sg = subgen()
g = delegator(sg)

g.send(1)
try: 
    g.send(2)
except StopIteration as e:
    print('1. Done!', e)

# 2 вариант:
sg = subgen()
g = delegator(sg)
g.send(1)
try:
    g.throw(CustomException)
except StopIteration as e:
    print('2. Done', e)


# Реализация без yield from.
@coroutine
def subgen():
    while True:
        try:
            message = yield
        except CustomException:
            print('CustomException from subgen')
        else:
            print('send', message)


@coroutine
def delegator(g):
    while True:
        try:
            data = yield
            g.send(data)
        except CustomException as e:
            print('CustomException from delegator')
            g.throw(e)


sg = subgen()
g = delegator(sg)

g.send(1)
g.send(2)
g.throw(CustomException)
