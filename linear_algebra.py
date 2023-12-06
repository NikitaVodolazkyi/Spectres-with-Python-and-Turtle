from __future__ import annotations
from multimethod import multimethod
from math import *


class Point:
    """
    3-dimensional vector, represents a point in xy-plane
    (x, y, 1) transpose
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Point:
        return Point(scalar * self.x, scalar * self.y)

    def __rmul__(self, scalar: float) -> Point:
        return self.__mul__(scalar)


class Matrix:
    """
    3x3 special type matrix:

    |a b c|
    |d e f|
    |0 0 1|

    acts on (x, y, 1) plane as
    |a b|
    |d e|  acts on (x, y)
    but with translation by (e, f)
    """

    def __init__(self, entries: list | tuple):
        self._entries = entries
        self._inverse = None

    # Return i,j th entry of the matrix
    # Note: indices go from 1 to 3 instead of from 0 to 2
    def __call__(self, i: int, j: int) -> float | int:
        try:
            return self._entries[j + 3 * i - 4]
        except IndexError:
            if i == 3:
                return (0, 0, 1)[j - 1]
            raise IndexError

    # Matrix inverse
    # It is faster than numpy but the inverses are not used in the code
    @property
    def inv(self) -> Matrix:
        if self._inverse is None:
            M = self
            det = M(1, 1) * M(2, 2) - M(1, 2) * M(1, 3)
            self._inverse = (1 / det) * Matrix([M(2, 2), -M(1, 2), (M(1, 2) * M(2, 3) - M(1, 3) * M(2, 2)),
                                                -M(2, 1), M(1, 1), (M(1, 3) * M(2, 1) - M(1, 1) * M(2, 3))])

        return self._inverse

    # Matrix multiplication, not commutative
    # Unfortunately is 6 times slower than numpy (which looses about half a second sometimes)
    @multimethod
    def __mul__(self, other: Matrix) -> Matrix:
        A, B = self, other
        return Matrix([A(1, 1) * B(1, 1) + A(1, 2) * B(2, 1),
                       A(1, 1) * B(1, 2) + A(1, 2) * B(2, 2),
                       A(1, 1) * B(1, 3) + A(1, 2) * B(2, 3) + A(1, 3),

                       A(2, 1) * B(1, 1) + A(2, 2) * B(2, 1),
                       A(2, 1) * B(1, 2) + A(2, 2) * B(2, 2),
                       A(2, 1) * B(1, 3) + A(2, 2) * B(2, 3) + A(2, 3)])

    # scalar * Matrix multiplication
    @multimethod
    def __mul__(self, other: int | float) -> Matrix:
        return Matrix([other * entry for entry in self._entries])

    # Applying matrix to the vector (that represents a point) (x, y, 1)-transpose
    @multimethod
    def __mul__(self, other: Point) -> Point:
        M = self._entries
        return Point(M[0] * other.x + M[1] * other.y + M[2], M[3] * other.x + M[4] * other.y + M[5])

    def __rmul__(self, other: float):
        return self.__mul__(other)

    # Rotation matrix
    @staticmethod
    def rot(ang: float) -> Matrix:
        c = cos(ang)
        s = sin(ang)
        return Matrix([c, -s, 0, s, c, 0])

    # Translation matrix
    @staticmethod
    def trans(tx: float, ty: float) -> Matrix:
        return Matrix([1, 0, tx, 0, 1, ty])

    def get_entries(self):
        print(self._entries)


IDENT = Matrix([1, 0, 0, 0, 1, 0])


def trans_to(p, q):
    res = q - p
    return Matrix.trans(res.x, res.y)

# Useful functions, currently not in use:

# def pframe(o: Point, p: Point, q: Point, a: float, b: float) -> Point:
#     return Point(o.x + a * p.x + b * q.x, o.y + a * p.y + b * q.y)
#
#
# def rotAbout(p, ang):
#     return Matrix.trans(p.x, p.y) * Matrix.rot(ang) * Matrix.trans(-p.x, -p.y)
#
#
# # Match unit interval to line segment p->q
# def matchSeg(p, q) -> Matrix:
#     return Matrix([q["x"] - p["x"], p["y"] - q["y"], p["x"], q["y"] - p["y"], q["x"] - p["x"], p["y"]])
#
#
# # Match line segment p1->q1 to line segment p2->q2
# def matchTwo(p1, q1, p2, q2) -> Matrix:
#     return matchSeg(p2, q2) * matchSeg(p1, q1).inv
