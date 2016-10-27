from geodude.utils import Point, side, Side
from geodude.convex_hull import graham_scan, quickhull, gift_wrapping
from hypothesis import given
from hypothesis.strategies import integers, lists, tuples


POINTS = [
    Point(0, 1),
    Point(3, 0),
    Point(3, 5),
    Point(6, 5),
    Point(8, 3),
    Point(7, 3),
    Point(6, 3),
    Point(4, 3),
    ]

HULL = {
    Point(0, 1),
    Point(3, 0),
    Point(3, 5),
    Point(6, 5),
    Point(8, 3),
    }


def test_common_graham_scan():
    assert set(graham_scan(POINTS)) == HULL


def test_common_gift_wrapping():
    assert set(gift_wrapping(POINTS)) == HULL


def test_common_quickhull():
    assert set(quickhull(POINTS)) == HULL


def bruteforce_hull(points):
    hull = set()
    for p in points:
        for q in points:
            valid = True
            if p == q:
                continue
            for r in points:
                if r == p or r == q:
                    continue
                if side(p, q, r) == Side.left:
                    valid = False
                    break
            if valid:
                hull.add(p)
                hull.add(q)
    return hull


@given(lists(
    tuples(integers(min_value=0, max_value=10), integers(min_value=0, max_value=10)),
    min_size=3, max_size=10, unique=True
    ))
def test_bruteforce_hull(S):
    IMPLS = [
        graham_scan,
        quickhull,
        gift_wrapping,
    ]
    points = [Point(*p) for p in S]
    vertices = bruteforce_hull(points)
    a, b, c = [set(f(points)) for f in IMPLS]
    assert a == b == c
    assert a.issubset(vertices)
