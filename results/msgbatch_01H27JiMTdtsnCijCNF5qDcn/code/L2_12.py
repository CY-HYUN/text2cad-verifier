import cadquery as cq
import math

base = cq.Workplane("XY").circle(50).extrude(10)

R = 30  # pitch radius for circular array
n = 3
pts = [(R * math.cos(2 * math.pi * i / n), R * math.sin(2 * math.pi * i / n)) for i in range(n)]

result = base
for (x, y) in pts:
    frustum = (
        cq.Workplane("XY").workplane(offset=10).center(x, y).circle(10)
        .workplane(offset=15).circle(5)
        .loft(combine=True)
    )
    result = result.union(frustum)

# through holes, 5 mm diameter, at each frustum center
for (x, y) in pts:
    hole = cq.Workplane("XY").center(x, y).circle(2.5).extrude(30)
    result = result.cut(hole)
