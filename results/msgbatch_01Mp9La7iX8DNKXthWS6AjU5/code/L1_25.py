import cadquery as cq
import math

# Base cylinder: diameter 40, height 40
result = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Through hole: diameter 10, cut through the entire part from the top face
result = result.faces(">Z").workplane().circle(5.0).cutThruAll()

# Counterbore: diameter 20, depth 10 from the top face
counterbore = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .circle(10.0)
    .extrude(10.0)
)
result = result.cut(counterbore)
