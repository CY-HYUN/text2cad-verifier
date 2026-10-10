import cadquery as cq
import math

result = (
    cq.Workplane("XY")
    .circle(50)
    .circle(25)
    .extrude(5)
)
