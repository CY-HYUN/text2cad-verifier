import cadquery as cq
import math

# Hollow spherical shell made by revolving a half-annulus profile about the X axis
R_out = 25.0
R_in = 20.0

profile = (
    cq.Workplane("XY")
    .moveTo(-R_out, 0)
    .threePointArc((0, R_out), (R_out, 0))
    .lineTo(R_in, 0)
    .threePointArc((0, R_in), (-R_in, 0))
    .close()
)
shell = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Reference plane perpendicular to X, outside the sphere (x = 40)
# 20x20 square centered on the X axis, cut "through all" (passes through both walls)
cutter = (
    cq.Workplane("YZ", origin=(40, 0, 0))
    .rect(20, 20)
    .extrude(-100)  # x from 40 to -60, fully through the sphere
)

result = shell.cut(cutter)
