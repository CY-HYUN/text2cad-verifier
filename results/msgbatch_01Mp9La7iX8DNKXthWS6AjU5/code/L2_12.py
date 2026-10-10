import cadquery as cq
import math

# Base: 100 mm dia, 10 mm thick
base = cq.Workplane("XY").circle(50).extrude(10)

# Frustum: loft from 20 mm dia at z=10 to 10 mm dia at z=25 (15 mm above base top)
def frustum(x, y):
    return (cq.Workplane("XY").workplane(offset=10).center(x, y).circle(10)
            .workplane(offset=15).circle(5).loft(combine=True))

R = 30
result = base
pts = []
for i in range(3):
    a = math.radians(90 + i * 120)
    x, y = R * math.cos(a), R * math.sin(a)
    pts.append((x, y))
    result = result.union(frustum(x, y))

# Through holes, 5 mm dia, at the center of each frustum
for x, y in pts:
    hole = cq.Workplane("XY").center(x, y).circle(2.5).extrude(30)
    result = result.cut(hole)
