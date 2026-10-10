import cadquery as cq
import math

# Spine cubic Bezier control points (x, y)
P = [(0, 0), (30, 20), (100, 25), (150, 5)]

def bez(t, i):
    return ((1 - t) ** 3 * P[0][i] + 3 * (1 - t) ** 2 * t * P[1][i]
            + 3 * (1 - t) * t ** 2 * P[2][i] + t ** 3 * P[3][i])

def y_at_x(x):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if bez(mid, 0) < x:
            lo = mid
        else:
            hi = mid
    return bez((lo + hi) / 2, 1)

# (x, major axis (along Y), minor axis (along Z)); circles have equal axes
sections = [(0, 15, 15), (50, 25, 20), (100, 22, 18), (150, 20, 20)]

def make_wires(offset):
    wires = []
    for x, a, b in sections:
        y = y_at_x(x)
        pl = cq.Plane(origin=(x, y, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
        ra = a / 2 - offset
        rb = b / 2 - offset
        wp = cq.Workplane(pl)
        if abs(a - b) < 1e-9:
            w = wp.circle(ra).val()
        else:
            w = wp.ellipse(ra, rb).val()
        wires.append(w)
    return wires

outer = cq.Solid.makeLoft(make_wires(0.0))
inner = cq.Solid.makeLoft(make_wires(1.5))

result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
