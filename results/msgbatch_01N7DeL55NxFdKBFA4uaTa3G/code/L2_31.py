import cadquery as cq
import math

R_out = 25.0
R_in = 20.0

# Half-annulus profile in the XY plane (x >= 0), revolved around the Y axis
profile = (
    cq.Workplane("XY")
    .moveTo(0, -R_out)
    .threePointArc((R_out, 0), (0, R_out))
    .lineTo(0, R_in)
    .threePointArc((R_in, 0), (0, -R_in))
    .close()
)
shell = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Reference plane perpendicular to X, outside the sphere
offset = 40.0
plane = cq.Plane(origin=(offset, 0, 0), xDir=(0, 1, 0), normal=(-1, 0, 0))

# 20x20 square centred on the X axis, extruded "through all" toward the sphere
cutter = cq.Workplane(plane).rect(20, 20).extrude(2 * offset + 10)

result = shell.cut(cutter)
