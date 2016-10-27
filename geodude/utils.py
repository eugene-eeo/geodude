import math
from collections import namedtuple
from enum import Enum


Point = namedtuple('Point', 'x,y')
Side = Enum('Side', 'left, right, along')


def det(p, q, r):
    return (q.x*r.y - q.y*r.x) - (p.x*r.y - p.y*r.x) + (p.x*q.y - p.y*q.x)


def side(p, q, r):
    v = det(p, q, r)
    if v == 0:
        return Side.along
    if v < 0:
        return Side.right
    return Side.left


def distance(p, q, r):
    dy = (q.y - p.y)
    dx = (q.x - p.x)
    top = abs(dy*r.x - dx*r.y + q.x*p.y - q.y*p.x)
    return top / math.sqrt(dx*dx + dy*dy)
