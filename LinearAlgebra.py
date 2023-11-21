from math import *

ident = [1, 0, 0, 0, 1, 0]


def pt(x, y):
    return {"x": x, "y": y}


# Affine matrix inverse
def inv(T):
    det = T[0] * T[4] - T[1] * T[3]
    return [T[4] / det, -T[1] / det, (T[1] * T[5] - T[2] * T[4]) / det,
            -T[3] / det, T[0] / det, (T[2] * T[3] - T[0] * T[5]) / det]


# Affine matrix multiply function
def mul(A, B):
    return [A[0] * B[0] + A[1] * B[3],
            A[0] * B[1] + A[1] * B[4],
            A[0] * B[2] + A[1] * B[5] + A[2],

            A[3] * B[0] + A[4] * B[3],
            A[3] * B[1] + A[4] * B[4],
            A[3] * B[2] + A[4] * B[5] + A[5]]


# !
def padd(p, q):
    return {"x": p["x"] + q["x"], "y": p["y"] + q["y"]}


# !
def psub(p, q):
    return {"x": p["x"] - q["x"], "y": p["y"] - q["y"]}


def pframe(o, p, q, a, b):
    return {"x": o["x"] + a * p["x"] + b * q["x"], "y": o["y"] + a * p["y"] + b * q["y"]}


# Rotation matrix
def trot(ang):
    c = cos(ang)
    s = sin(ang)
    return [c, -s, 0, s, c, 0]


# Translation matrix
def ttrans(tx, ty):
    return [1, 0, tx, 0, 1, ty]


def transTo(p, q):
    return ttrans(q["x"] - p["x"], q["y"] - p["y"])


def rotAbout(p, ang):
    return mul(ttrans(p["x"], p["y"]),
               mul(trot(ang), ttrans(-p["x"], -p["y"])))


# Matrix * point
def transPt(M, P):
    return pt(M[0] * P["x"] + M[1] * P["y"] + M[2], M[3] * P["x"] + M[4] * P["y"] + M[5])


# Match unit interval to line segment p->q
def matchSeg(p, q):
    return [q["x"] - p["x"], p["y"] - q["y"], p["x"], q["y"] - p["y"], q["x"] - p["x"], p["y"]]


# Match line segment p1->q1 to line segment p2->q2
def matchTwo(p1, q1, p2, q2):
    return mul(matchSeg(p2, q2), inv(matchSeg(p1, q1)))
