import cadquery as cq
import math

P = [(0, 0), (30, 20), (100, 25), (150, 5)]

def bez(t):
    u = 1 - t
    x = u**3*P[0][0] + 3*u*u*t*P[1][0] + 3*u*t*t*P[2][0] + t**3*P[3][0]
    y = u**3*P[0][1] + 3*u*u*t*P[1][1] + 3*u*t*t*P[2][1] + t**3*P[3][1]
    return x, y

def y_at_x(xt):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if bez(m)[0] < xt:
            lo = m
        else:
            hi = m
    return bez(0.5 * (lo + hi))[1]

# (x, half-height along Y (minor), half-width along Z (major))
sections = [
    (0.0, 7.5, 7.5),
    (50.0, 10.0, 12.5),
    (100.0, 9.0, 11.0),
    (150.0, 10.0, 10.0),
]

def wire(x, ry, rz):
    y = y_at_x(x)
    return cq.Workplane("YZ", origin=(x, y, 0)).ellipse(ry, rz).val()

t = 1.5
outer_wires = [wire(x, a, b) for (x, a, b) in sections]
outer = cq.Solid.makeLoft(outer_wires, False)

inner_secs = [
    (t, 7.5 - t + (10.0 - 7.5) * t / 50.0, 7.5 - t + (12.5 - 7.5) * t / 50.0),
    (50.0, 10.0 - t, 12.5 - t),
    (100.0, 9.0 - t, 11.0 - t),
    (150.0 - t, 10.0 - t, 10.0 - t),
]
inner_wires = [wire(x, a, b) for (x, a, b) in inner_secs]
inner = cq.Solid.makeLoft(inner_wires, False)

result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
