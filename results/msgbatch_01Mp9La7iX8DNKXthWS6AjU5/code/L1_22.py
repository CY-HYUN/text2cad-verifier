import cadquery as cq
import math

frustum = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .workplane(offset=30.0)
    .rect(40.0, 40.0)
    .loft(combine=True)
)

hole = cq.Workplane("XY").circle(10.0).extrude(30.0)

result = frustum.cut(hole)
