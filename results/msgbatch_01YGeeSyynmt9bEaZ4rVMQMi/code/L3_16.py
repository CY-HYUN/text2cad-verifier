import cadquery as cq
import math

# Longitudinal spine: cubic Bezier in XZ, P0(0,0,0) P1(20,0,35) P2(80,0,35) P3(110,0,0)
def spine_pt(t):
    a, b, c, d = (1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t**2, t**3
    x = b*20 + c*80 + d*110
    z = b*35 + c*35
    return x, z

def spine_height(x):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5*(lo+hi)
        if spine_pt(m)[0] < x:
            lo = m
        else:
            hi = m
    return spine_pt(0.5*(lo+hi))[1]

# Bottom contour (XY plane), asymmetric half widths
def half_widths(x):
    s = math.sin(math.pi * x / 110.0)
    base = 30.0 * (s ** 0.6)
    bias = 1.0 + 0.12 * math.sin(math.pi * x / 110.0 * 2)  # asymmetric bulge
    yl = max(base * 1.08 * bias, 3.0)
    yr = max(base * 0.92 / bias, 3.0)
    return yl, yr

def section(x, inset=0.0):
    h = max(spine_height(x) - inset, 2.0)
    yl, yr = half_widths(x)
    yl = max(yl - inset, 1.5)
    yr = max(yr - inset, 1.5)
    z0 = inset * 0.0
    pts = [
        cq.Vector(x, -yl, z0),
        cq.Vector(x, -yl * 0.75, z0 + h * 0.7),
        cq.Vector(x, 0, z0 + h),
        cq.Vector(x, yr * 0.75, z0 + h * 0.7),
        cq.Vector(x, yr, z0),
    ]
    arch = cq.Edge.makeSpline(pts)
    base = cq.Edge.makeLine(pts[-1], pts[0])
    return cq.Wire.assembleEdges([arch, base])

xs = [3, 20, 40, 60, 80, 95, 107]
wires = [section(x) for x in xs]
outer = cq.Solid.makeLoft(wires, False)
body = cq.Workplane("XY").add(outer)

try:
    result = body.faces("<Z").shell(-2.0)
    if not result.val().isValid():
        raise ValueError
except Exception:
    inner_xs = [5, 20, 40, 60, 80, 95, 105]
    inner = cq.Solid.makeLoft([section(x, 2.0) for x in inner_xs], False)
    inner = inner.translate(cq.Vector(0, 0, -0.01))
    result = body.cut(cq.Workplane("XY").add(inner))
