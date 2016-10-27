import math
from geodude.utils import distance, side, Side, distance2


def _findhull(points, A, B):
    if not points:
        return
    M = max(points, key=lambda p: distance(A, B, p))
    yield M
    L = []
    R = []
    for p in points:
        if p == M:
            continue
        if side(A, M, p) == Side.right: L.append(p)
        elif side(M, B, p) == Side.right: R.append(p)
    yield from _findhull(L, A, M)
    yield from _findhull(R, M, B)


def quickhull(points):
    points = sorted(points)
    l, *mid, r = points
    L = []
    R = []
    for p in mid:
        s = side(l, r, p)
        if s == Side.right: R.append(p)
        elif s == Side.left: L.append(p)
    yield l
    yield from _findhull(R, l, r)
    yield from _findhull(L, r, l)
    yield r


def gift_wrapping(points):
    A = min(points)
    I = A  # initial endpoint
    while True:
        yield A
        end = points[0]
        for p in points:
            s = side(A, end, p)
            if end == A or s == Side.left or \
                    (s == Side.along and distance2(A, p) > distance2(A, end)):
                end = p
        if end == I:
            break
        A = end


def graham_scan(points):
    S = sorted(points)
    U = [S[0], S[1]]
    for p in S[2:]:
        U.append(p)
        while len(U) > 2 and side(U[-3], U[-2], U[-1]) != Side.right:
            del U[-2]
    L = [S[-1], S[-2]]
    for p in reversed(S[:-2]):
        L.append(p)
        while len(L) > 2 and side(L[-3], L[-2], L[-1]) != Side.right:
            del L[-2]
    del L[0]
    del L[-1]
    return U + L
