import cadquery as cq
import math

# Spine cubic Bezier (XY plane)
P = [(0, 0), (30, 20), (100, 25), (150, 5)]

def bez(t):
    u = 1 - t
    x = 3*u*u*t*P[1][0] + 3*u*t*t*P[2][0] + t**3*P[3][0]
    y = 3*u*u*t*P[1][1] + 3*u*t*t*P[2][1] + t**3*P[3][1]
    return x, y

def y_at_x(xt):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if bez(mid)[0] < xt:
            lo = mid
        else:
            hi = mid
    return bez((lo + hi) / 2)[1]

# (x, half-width along Y, half-height along Z)
secs = [
    (0,   7.5, 7.5),
    (50,  10.0, 12.5),
    (100, 9.0, 11.0),
    (150, 10.0, 10.0),
]

def make_wires(t):
    wires = []
    for x, a, b in secs:
        a2 = max(a - t, 0.5)
        b2 = max(b - t, 0.5)
        yc = y_at_x(x)
        wp = cq.Workplane("YZ", origin=(x, yc, 0))
        if abs(a - b) < 1e-9:
            w = wp.circle(a2).val()
        else:
            w = wp.ellipse(a2, b2).val()
        wires.append(w)
    return wires

outer = cq.Solid.makeLoft(make_wires(0.0), True)
inner = cq.Solid.makeLoft(make_wires(1.5), True)

result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
