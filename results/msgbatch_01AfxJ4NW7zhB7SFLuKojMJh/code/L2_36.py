import cadquery as cq
import math

thickness = 20.0
ring = (
    cq.Workplane("XY")
    .circle(60.0)
    .circle(40.0)
    .extrude(thickness)
)

pts = [
    (50.0 * math.cos(math.radians(i * 60)), 50.0 * math.sin(math.radians(i * 60)))
    for i in range(6)
]

# Through holes (6 mm diameter)
through = (
    cq.Workplane("XY")
    .pushPoints(pts)
    .circle(3.0)
    .extrude(thickness)
)

# Counterbores (10 mm diameter, 10 mm deep) from the top face
cbore = (
    cq.Workplane("XY")
    .workplane(offset=thickness - 10.0)
    .pushPoints(pts)
    .circle(5.0)
    .extrude(10.0)
)

result = ring.cut(through).cut(cbore)
