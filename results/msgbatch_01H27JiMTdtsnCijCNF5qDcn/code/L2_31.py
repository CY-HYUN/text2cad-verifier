import cadquery as cq
import math

# Hollow spherical shell made by revolving a half-annulus profile about the X axis
ro = 25.0
ri = 20.0
profile = (
    cq.Workplane("XY")
    .moveTo(-ro, 0)
    .threePointArc((0, ro), (ro, 0))
    .lineTo(ri, 0)
    .threePointArc((0, ri), (-ri, 0))
    .close()
)
shell = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Reference plane perpendicular to X, outside the sphere (x = 40)
# Square 20x20 centered on the X axis, extruded through all toward the sphere (-X direction)
# Only cut through the +X side wall (through all in one direction)
cutter = (
    cq.Workplane("YZ", origin=(40, 0, 0))
    .rect(20, 20)
    .extrude(-100)  # through all, passing in -X direction
)

# Limit to cutting the near wall only? "Through all" cuts both walls; keep that behavior.
result = shell.cut(cutter)
