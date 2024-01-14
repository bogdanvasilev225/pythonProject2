from random import randint, randrange


def randbool(r, mxr):
    return randint(0, mxr) <= r


def randcell(w, h):
    return (randint(0, w - 1), randint(0, h - 1))


def randcell2(x, y):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    t = randrange(4)
    dx, dy = moves[t][0], moves[t][1]
    return (x + dx, y + dy)
