from .utils import line_segment_distance, side, Side, distance


def _findhull(points, A, B):
    if not points:
        return
    M = max(points, key=lambda p: line_segment_distance(A, B, p))
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
            if end == A or \
                    s == Side.left or \
                    (s == Side.along and distance(A, p) > distance(A, end)):
                end = p
        if end == I:
            break
        A = end


def _until_all_right(S):
    H = [S[0], S[1]]
    for p in S[2:]:
        H.append(p)
        while len(H) > 2 and side(H[-3], H[-2], H[-1]) != Side.right:
            del H[-2]
    return H


def graham_scan(points):
    S = sorted(points)
    upper = _until_all_right(S)
    S.reverse()
    lower = _until_all_right(S)
    del lower[0]
    del lower[-1]
    return upper + lower
