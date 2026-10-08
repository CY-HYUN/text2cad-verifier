import cadquery as cq
import math

# Cubic Bezier guide curve in XZ plane
P = [(0.0, 0.0), (30.0, 20.0), (100.0, 25.0), (150.0, 5.0)]

def bez(t):
    mt = 1 - t
    x = mt**3*P[0][0] + 3*mt**2*t*P[1][0] + 3*mt*t**2*P[2][0] + t**3*P[3][0]
    z = mt**3*P[0][1] + 3*mt**2*t*P[1][1] + 3*mt*t**2*P[2][1] + t**3*P[3][1]
    return x, z

def z_at_x(xt):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if bez(mid)[0] < xt:
            lo = mid
        else:
            hi = mid
    return bez(0.5*(lo+hi))[1]

# Sections: (x, semi-axis Y, semi-axis Z)
sections = [
    (0.0, 7.5, 7.5),
    (50.0, 12.5, 10.0),
    (100.0, 11.0, 9.0),
    (150.0, 10.0, 10.0),
]

def make_wire(x, a, b, off=0.0):
    z = z_at_x(x)
    c = cq.Vector(x, 0, z)
    n = cq.Vector(1, 0, 0)
    a2, b2 = a - off, b - off
    if abs(a2 - b2) < 1e-6:
        return cq.Wire.makeEllipse(a2 + 1e-4, b2, c, n, cq.Vector(0, 1, 0))
    if a2 >= b2:
        return cq.Wire.makeEllipse(a2, b2, c, n, cq.Vector(0, 1, 0))
    return cq.Wire.makeEllipse(b2, a2, c, n, cq.Vector(0, 0, 1))

outer_wires = [make_wire(*s) for s in sections]
outer = cq.Solid.makeLoft(outer_wires, False)

result = None
try:
    shelled = cq.Workplane("XY").add(outer).faces("<X or >X").shell(-1.5)
    if shelled.val().isValid() and shelled.val().Volume() > 1.0:
        result = shelled
except Exception:
    result = None

if result is None:
    # Fallback: subtract an inner loft, extended slightly past ends
    inner_wires = [make_wire(*s, off=1.5) for s in sections]
    inner = cq.Solid.makeLoft(inner_wires, False)
    cutter = cq.Workplane("XY").add(inner)
    # extend openings at the ends
    z0 = z_at_x(0.0)
    z3 = z_at_x(150.0)
    cap0 = (cq.Workplane("YZ", origin=(-1, 0, z0)).circle(7.5 - 1.5).extrude(1.01))
    cap3 = (cq.Workplane("YZ", origin=(149.99, 0, z3)).circle(10.0 - 1.5).extrude(1.01))
    cutter = cutter.union(cap0).union(cap3)
    result = cq.Workplane("XY").add(outer).cut(cutter)
