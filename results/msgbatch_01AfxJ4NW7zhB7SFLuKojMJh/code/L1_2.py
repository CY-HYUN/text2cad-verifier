import cadquery as cq
import math

# Hollow cylinder: OD 40, ID 25, length 120 along Z axis
result = (
    cq.Workplane("XY")
    .circle(20.0)
    .circle(12.5)
    .extrude(120.0)
)
