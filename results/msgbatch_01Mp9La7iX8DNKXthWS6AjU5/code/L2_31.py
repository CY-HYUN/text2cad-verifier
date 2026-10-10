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
# Square 20x20 centered on X axis, extruded through all along -X direction
# Plane normal +X; local x -> Y, local y -> Z
cutter = (
    cq.Workplane("YZ", origin=(40, 0, 0))
    .rect(20, 20)
    .extrude(-100)  # through all, toward -X, passing through both walls
)

# Through all would cut both sides; the described window is at the curved edge
# on the side of the plane, so limit the cut to the near wall (x > 0)
cutter = (
    cq.Workplane("YZ", origin=(40, 0, 0))
    .rect(20, 20)
    .extrude(-40)  # from x=40 to x=0, through the near wall only
)

result = shell.cut(cutter)
