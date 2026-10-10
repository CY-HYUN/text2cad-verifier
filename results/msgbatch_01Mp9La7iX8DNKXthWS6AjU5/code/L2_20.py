import cadquery as cq
import math

cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

center = (25, 25, 25)
plane = cq.Plane(origin=center, xDir=(1, -1, 0), normal=(1, 1, 1))

cutter = (
    cq.Workplane(plane)
    .circle(5)
    .extrude(100, both=True)
)

result = cube.cut(cutter)
