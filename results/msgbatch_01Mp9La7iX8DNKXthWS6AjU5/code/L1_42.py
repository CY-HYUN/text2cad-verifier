import cadquery as cq
import math

cyl = cq.Workplane("XY").circle(15.0).extrude(50.0)

cutter = (
    cq.Workplane("XY")
    .rect(200, 200)
    .extrude(200)
    .rotate((0, 0, 0), (0, 1, 0), 30)
    .translate((-15, 0, 50))
)

result = cyl.cut(cutter)
