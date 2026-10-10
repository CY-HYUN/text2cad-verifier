import cadquery as cq
import math

R = 15.0
depth = 1.0
L = 60.0
M = 48          # divisions around circumference (~1.96 mm arc step)
J = 30          # divisions along length (2 mm step)

dth = 2 * math.pi / M
dz = L / J


def rad(i, j):
    # apex (full radius) where i+j is odd, away from the end rows; otherwise groove bottom
    if 0 < j < J and (i + j) % 2 == 1:
        return R
    return R - depth


def P(i, j):
    i %= M
    r = rad(i, j)
    a = i * dth
    return cq.Vector(r * math.cos(a), r * math.sin(a), j * dz)


def is_apex(i, j):
    return rad(i % M, j) == R


def tri(a, b, c):
    w = cq.Wire.makePolygon([a, b, c, a])
    return cq.Face.makeFromWires(w)


faces = []
for j in range(J):
    for i in range(M):
        c00 = (i, j)
        c10 = (i + 1, j)
        c11 = (i + 1, j + 1)
        c01 = (i, j + 1)
        # choose the diagonal that connects two groove-bottom points
        if not is_apex(*c00) and not is_apex(*c11):
            faces.append(tri(P(*c00), P(*c10), P(*c11)))
            faces.append(tri(P(*c00), P(*c11), P(*c01)))
        else:
            faces.append(tri(P(*c00), P(*c10), P(*c01)))
            faces.append(tri(P(*c10), P(*c11), P(*c01)))

# end caps (planar regular polygons)
bot = [P(i, 0) for i in range(M)]
top = [P(i, J) for i in range(M)]
faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon(bot[::-1] + [bot[-1]])))
faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon(top + [top[0]])))

shell