import cadquery as cq
import math

# Base: 100 mm diameter disc, 10 mm thick
base = cq.Workplane("XY").circle(50).extrude(10)

# Frustum: loft from 20 mm dia (on top of base) to 10 mm dia (15 mm above)
R = 30.0  # radius of circular pattern
frustums = None
pts = []
for i in range(3):
    a = math.radians(i * 120)
    x, y = R * math.cos(a), R * math.sin(a)
    pts.append((x, y))
    f = (cq.Workplane("XY").workplane(offset=10).center(x, y)
         .circle(10)
         .workplane(offset=15).circle(5)
         .loft(combine=True))
    frustums = f if frustums is None else frustums.union(f)

result = base.union(frustums)

# Through holes: 5 mm diameter at each frustum center
holes = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints(pts).circle(2.5).extrude(30))
result = result.cut(holes)
