import cadquery as cq
import math

H = 150.0
N_PTS = 72
N_SEC = 21

def section(z):
    t = z / H
    s = math.sin(math.pi * t)
    amp = 5.0 * s
    if t <= 0.5:
        r0 = 30.0 + 5.0 * s
    else:
        r0 = 40.0 - 5.0 * s
    pts = []
    for i in range(N_PTS):
        th = 2 * math.pi * i / N_PTS
        r = r0 + amp * math.cos(6 * th)
        pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))
    e = cq.Edge.makeSpline(pts, periodic=True)
    return cq.Wire.assembleEdges([e])

wires = [section(H * k / (N_SEC - 1)) for k in range(N_SEC)]
solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
