import cadquery as cq
import math

H = 150.0
N = 60          # points per section
NS = 11         # number of loft sections

wires = []
for i in range(NS):
    t = i / (NS - 1)
    z = H * t
    r0 = 30 + 10 * t                      # mean radius: 30 -> 35 (at mid) -> 40
    amp = 5.0 * math.sin(math.pi * t)     # 0 at ends, 5 mm at mid-height
    pts = []
    for k in range(N):
        th = 2 * math.pi * k / N
        r = r0 + amp * math.cos(6 * th)   # peak aligned with +X
        pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))
    edge = cq.Edge.makeSpline(pts, periodic=True)
    wires.append(cq.Wire.assembleEdges([edge]))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
