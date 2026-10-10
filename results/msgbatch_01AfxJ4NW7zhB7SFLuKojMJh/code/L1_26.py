import cadquery as cq
import math

R = 30.0
h = 15.0

sphere = cq.Workplane("XY").sphere(R)

# Remove everything above z = 15
cutter = (
    cq.Workplane("XY")
    .workplane(offset=h)
    .rect(4 * R, 4 * R)
    .extrude(2 * R)
)

result = sphere.cut(cutter)
