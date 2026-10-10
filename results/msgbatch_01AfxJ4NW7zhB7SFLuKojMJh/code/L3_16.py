import cadquery as cq
import math

def bez(t):
    x = 3*(1-t)**2*t*20 + 3*(1-t)*t**2*80 + t**3*110
    z = 3*(1-t)**2*t*35 + 3*(1-t)*t**2*35
    return x, z

def spine_z(x):
    lo, hi = 0.0, 1.0
    for _ in range(50):
        m = (lo + hi) / 2
        if bez(m)[0] < x:
            lo = m
        else:
            hi = m
    return bez(lo)[1]

def half_w(x):
    return 10 + 20 * math.exp(-((x - 73) / 40.0) ** 2)

def section(x, w, h, zoff=0.0):
    pts = []
    n = 12
    for i in range(n + 1):
        th = math.pi * i / n
        y = -w * math.cos(th) + 3.0 * math.sin(th)   # asymmetric hump toward +y
        z = h * (math.sin(th) ** 0.6) + zoff
        pts.append(cq.Vector(x, y, z))
    spl = cq.Edge.makeSpline(pts)
    line = cq.Edge.makeLine(pts[-1], pts[0])
    return cq.Wire.assembleEdges([spl, line])

def build(x0, x1, n, dw, dh, zoff):
    wires = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        h = max(spine_z(x), 3.0) - dh
        w = half_w(x) - dw
        wires.append(section(x, w, max(h, 1.0), zoff))
    return cq.Workplane("XY").add(cq.Solid.makeLoft(wires, False))

outer = build(3, 107, 12, 0, 0, 0)
inner = build(6, 104, 12, 2.0, 1.0, -1.0)

shell = outer.cut(inner)

# concave thumb rest on the left (-Y) side
thumb = cq.Workplane("XY").sphere(13).translate((42, -25, 13))
result = shell.cut(thumb)
