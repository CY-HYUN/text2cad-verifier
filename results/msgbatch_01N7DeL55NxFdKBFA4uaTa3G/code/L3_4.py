import cadquery as cq
import math

# Bezier guide curve in XZ plane: P0(0,0), P1(30,20), P2(100,25), P3(150,5)
P = [(0.0, 0.0), (30.0, 20.0), (100.0, 25.0), (150.0, 5.0)]

def bez(t):
    mt = 1 - t
    x = mt**3*P[0][0] + 3*mt*mt*t*P[1][0] + 3*mt*t*t*P[2][0] + t**3*P[3][0]
    z = mt**3*P[0][1] + 3*mt*mt*t*P[1][1] + 3*mt*t*t*P[2][1] + t**3*P[3][1]
    return x, z

def z_at_x(xt):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if bez(m)[0] < xt:
            lo = m
        else:
            hi = m
    return bez(0.5 * (lo + hi))[1]

# Sections: (x, semi-axis along Z, semi-axis along Y)
sections = [
    (0.0, 7.5, 7.5),      # circle D15
    (50.0, 12.5, 10.0),   # ellipse 25 x 20
    (100.0, 11.0, 9.0),   # ellipse 22 x 18
    (150.0, 10.0, 10.0),  # circle D20
]

def make_wires(offset=0.0):
    wires = []
    for x, a, b in sections:
        z = z_at_x(x)
        wires.append(
            cq.Wire.makeEllipse(
                a - offset, b - offset,
                cq.Vector(x, 0, z),
                cq.Vector(1, 0, 0),
                cq.Vector(0, 0, 1),
            )
        )
    return wires

outer = cq.Solid.makeLoft(make_wires(0.0), False)

result = None
try:
    shelled = cq.Workplane("XY").add(outer).faces("<X or >X").shell(-1.5)
    if shelled.val().isValid():
        result = shelled
except Exception:
    result = None

if result is None:
    inner = cq.Solid.makeLoft(make_wires(1.5), False)
    result = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))
