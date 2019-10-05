def gen1(value):
    for i in value:
        yield i


def gen2(value):
    for i in range(value):
        yield i


g1 = gen1('robin')
g2 = gen2(5)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
