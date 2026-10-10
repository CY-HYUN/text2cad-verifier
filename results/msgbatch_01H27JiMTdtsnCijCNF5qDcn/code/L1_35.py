import cadquery as cq
import math

cyl = cq.Workplane("XY").circle(20.0).extrude(40.0)

cone = (
    cq.Workplane("XZ")
    .polyline([(0, 40), (15, 40), (0, 25)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(cone)
