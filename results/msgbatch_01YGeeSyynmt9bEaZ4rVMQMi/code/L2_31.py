import cadquery as cq

R_out = 25.0
R_in = 20.0

# Half-annulus profile in the XY plane (y >= 0), revolved 360 deg about the X axis
profile = (
    cq.Workplane("XY")
    .moveTo(-R_out, 0)
    .threePointArc((0, R_out), (R_out, 0))
    .lineTo(R_in, 0)
    .threePointArc((0, R_in), (-R_in, 0))
    .close()
)
shell = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Reference plane perpendicular to X, outside the sphere (x = 30)
plane_x = 30.0
cutter = (
    cq.Workplane("YZ", origin=(plane_x, 0, 0))
    .rect(20, 20)
    .extrude(-2 * plane_x)  # through all toward -X
)

result = shell.cut(cutter)
