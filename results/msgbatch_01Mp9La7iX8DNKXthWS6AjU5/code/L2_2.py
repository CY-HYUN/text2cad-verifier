import cadquery as cq
import math

# Sphere of radius 40 centered at origin
sphere = cq.Workplane("XY").sphere(40)

# Cylinder: diameter 30, axis parallel to Z, offset 25 mm in X, through all (both directions)
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-100)
    .center(25, 0)
    .circle(15)
    .extrude(200)
)

result = sphere.cut(cutter)
