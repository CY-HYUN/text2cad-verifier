import cadquery as cq
import math

# Base cylinder: diameter 60 mm, height 40 mm
cylinder = cq.Workplane("XY").circle(30.0).extrude(40.0)

# Eccentric through hole: diameter 10 mm, offset 15 mm in +X, cut from the top face
result = (
    cylinder.faces(">Z").workplane(origin=(0, 0, 40.0))
    .center(15.0, 0)
    .circle(5.0)
    .cutThruAll()
)
