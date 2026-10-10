import cadquery as cq
import math

disc = cq.Workplane("XY").circle(50).extrude(10)

R = 30
result = disc
for i in range(3):
    a = math.radians(90 + 120 * i)
    x, y = R * math.cos(a), R * math.sin(a)
    cone = (cq.Workplane("XY").workplane(offset=10).center(x, y)
            .circle(10).workplane(offset=15).circle(5).loft(combine=True))
    result = result.union(cone)

for i in range(3):
    a = math.radians(90 + 120 * i)
    x, y = R * math.cos(a), R * math.sin(a)
    hole = cq.Workplane("XY").center(x, y).circle(2.5).extrude(25)
    result = result.cut(hole)
