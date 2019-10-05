def init_generator(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class CustomException(Exception):
    pass


@init_generator
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
        except CustomException:
            print('CustomException')
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)


g = average()
print(g.send(10))
print(g.send(40))
print(g.throw(CustomException))
print(g.throw(StopIteration))


@init_generator
def average_two():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
        except CustomException:
            print('CustomException')
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)

    return average


g = average_two()
print(g.send(10))
print(g.send(40))
print(g.throw(StopIteration))
try:
    g.throw(CustomException)
except StopIteration as e:
    print('Done!', e.value)



