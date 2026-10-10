import cadquery as cq
import math

P = [(0, 0), (30, 20), (100, 25), (150, 5)]

def bez(t):
    mt = 1 - t
    b = [mt**3, 3*mt*mt*t, 3*mt*t*t, t**3]
    return (sum(b[i]*P[i][0] for i in range(4)),
            sum(b[i]*P[i][1] for i in range(4)))

def t_for_x(xt):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5*(lo+hi)
        if bez(m)[0] < xt:
            lo = m
        else:
            hi = m
    return 0.5*(lo+hi)

# (x, major diameter (Z), minor diameter (Y))
sections = [(0, 15, 15), (50, 25, 20), (100, 22, 18), (150, 20, 20)]
wall = 1.5

def make_wire(x, dmaj, dmin, off):
    t = t_for_x(x)
    _, y = bez(t)
    pl = cq.Plane(origin=(x, y, 0), xDir=(0, 0, 1), normal=(1, 0, 0))
    a = dmaj/2 - off
    b = dmin/2 - off
    wp = cq.Workplane(pl)
    if abs(a - b) < 1e-6:
        w = wp.circle(a).wires().val()
    else:
        w = wp.ellipse(a, b).wires().val()
    return w

outer_w = [make_wire(x, a, b, 0) for x, a, b in sections]
inner_w = [make_wire(x, a, b, wall) for x, a, b in sections]

outer = cq.Solid.makeLoft(outer_w, False)
inner = cq.Solid.makeLoft(inner_w, False)

result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
