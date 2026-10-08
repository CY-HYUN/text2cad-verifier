import cadquery as cq
import math

# Longitudinal spine: cubic Bezier in XZ with points (0,0),(20,35),(80,35),(110,0)
P = [(0.0, 0.0), (20.0, 35.0), (80.0, 35.0), (110.0, 0.0)]

def bez(t):
    mt = 1 - t
    b = [mt**3, 3*mt*mt*t, 3*mt*t*t, t**3]
    x = sum(b[i]*P[i][0] for i in range(4))
    z = sum(b[i]*P[i][1] for i in range(4))
    return x, z

def spine_z(x):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5*(lo+hi)
        if bez(m)[0] < x:
            lo = m
        else:
            hi = m
    return max(bez(0.5*(lo+hi))[1], 6.0)

# Bottom contour (asymmetric) in XY: left and right half-widths
def w_left(x):
    s = math.sin(math.pi * x / 110.0)
    return 6.0 + 26.0 * s**0.7 * (1.0 + 0.15*math.cos(math.pi*x/110.0))

def w_right(x):
    s = math.sin(math.pi * x / 110.0)
    return 6.0 + 22.0 * s**0.8 * (1.0 - 0.1*math.cos(math.pi*x/110.0))

xs = [4, 20, 40, 60, 80, 95, 106]
wires = []
for x in xs:
    h = spine_z(x)
    wl = w_left(x)
    wr = w_right(x)
    pts = [
        cq.Vector(x, -wl, 0),
        cq.Vector(x, -wl*0.85, h*0.55),
        cq.Vector(x, -wl*0.45, h*0.92),
        cq.Vector(x, 0, h),
        cq.Vector(x, wr*0.45, h*0.92),
        cq.Vector(x, wr*0.85, h*0.55),
        cq.Vector(x, wr, 0),
    ]
    arch = cq.Edge.makeSpline(pts)
    base = cq.Edge.makeLine(pts[-1], pts[0])
    wires.append(cq.Wire.assembleEdges([arch, base]))

solid = cq.Solid.makeLoft(wires, False)
body = cq.Workplane("XY").add(solid)

try:
    result = body.faces("<Z").shell(-2.0)
    if not result.val().isValid():
        result = body
except Exception:
    result = body
