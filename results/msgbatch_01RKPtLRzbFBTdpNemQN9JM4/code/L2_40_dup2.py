import cadquery as cq
import math

R = 15.0
L = 60.0
n = 47  # starts: circumference ~94.25 / 2 mm spacing
lead = math.pi * 30.0  # 45 degree helix
twist = 360.0 * L / lead

body = cq.Workplane("XY").circle(R).extrude(L)

prof = [(14.0, 0.0), (15.0, 1.0), (15.5, 1.0), (15.5, -1.0), (15.0, -1.0)]

def cutter(sign):
    wp = cq.Workplane("XY")
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        pts = [(r * c - w * s, r * s + w * c) for r, w in prof]
        wp = wp.polyline(pts).close()
    return wp.twistExtrude(L, sign * twist)

result = body.cut(cutter(1)).cut(cutter(-1))
