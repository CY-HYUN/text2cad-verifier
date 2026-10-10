import cadquery as cq
import math

block = cq.Workplane("XY").box(60, 20, 30, centered=False)

# Cylinder along Y, centered at midpoint of bottom edge of front face
cutter = (
    cq.Workplane("XZ", origin=(30, 0, 0))
    .circle(20)
    .extrude(-20)  # XZ normal is -Y, so negative extrude goes toward +Y
)

result = block.cut(cutter)
