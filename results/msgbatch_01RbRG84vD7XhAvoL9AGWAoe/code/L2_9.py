import cadquery as cq
import math

r_root = 40.0
r_tip = 45.0
r_in = 25.0
thk = 10.0
n = 12

pts = []
for i in range(n):
    a = math.radians(i * 360.0 / n)
    pts.append((r_root * math.cos(a), r_root * math.sin(a)))
    pts.append((r_tip * math.cos(a), r_tip * math.sin(a)))

outer = cq.Workplane("XY").polyline(pts).close().extrude(thk)
hole = cq.Workplane("XY").circle(r_in).extrude(thk)
result = outer.cut(hole)
