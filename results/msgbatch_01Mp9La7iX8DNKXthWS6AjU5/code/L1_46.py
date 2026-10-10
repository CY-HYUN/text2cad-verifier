import cadquery as cq
import math

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (30.0, 0), (0, 40.0)])
    .close()
    .extrude(60.0)
)
