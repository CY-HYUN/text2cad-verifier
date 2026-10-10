import cadquery as cq
import math

# Longitudinal spine: cubic Bezier in the XZ plane
P = [(0, 0), (20, 35), (80, 35), (110, 0)]

def bez(t):
    u = 1 - t
    x = u**3*P[0][0] + 3*u*u*t*P[1][0] + 3*u*t*t*P[2][0] + t**3*P[3][0]
    z = u**3*P[0][1] + 3*u*u*t*P[1][1] + 3*u*t*t*P[2][1] + t**3*P[3][1]
    return x, z

def spine_z(x):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if bez(mid)[0] < x:
            lo = mid
        else:
            hi = mid
    return bez((lo + hi) / 2)[1]

# Bottom contour (asymmetric) in XY: right and left edges
def y_right(x):
    s = math.sin(math.pi * x / 110.0)
    return (24 + 4 * math.sin(math.pi * x / 110.0 * 2)) * max(s, 0) ** 0.6

def y_left(x):
    s = math.sin(math.pi * x / 110.0)
    return -(20 + 3 * math.cos(math.pi * x / 110.0)) * max(s, 0) ** 0.6

def section(x, inset, base_z):
    yl = y_left(x) + inset
    yr = y_right(x) - inset
    ym = (yl + yr) / 2
    z = spine_z(x) - inset
    V = cq.Vector
    a = V(x, yl, base_z)
    b = V(x, ym, z)
    c = V(x, yr, base_z)
    arc = cq.Edge.makeThreePointArc(a, b, c)
    line = cq.Edge.makeLine(c, a)
    return cq.Wire.assembleEdges([arc, line])

outer_x = [1, 40, 80, 109]
inner_x = [3, 40, 80, 107]

outer = cq.Solid.makeLoft([section(x, 0, 0) for x in outer_x])
inner = cq.Solid.makeLoft([section(x, 2.0, -0.5) for x in inner_x])

result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
