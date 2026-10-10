import cadquery as cq

# Cylinder: diameter 50, height 80
cyl = cq.Workplane("XY").circle(25.0).extrude(80.0)

# Groove cross-section on XZ plane: radial from r=20 to r=25, axial z=35..45
# Extend slightly outside the cylinder for a clean cut
groove_profile = (
    cq.Workplane("XZ")
    .polyline([(20.0, 35.0), (26.0, 35.0), (26.0, 45.0), (20.0, 45.0)])
    .close()
)
groove = groove_profile.revolve(360.0, (0, 0, 0), (0, 1, 0))

result = cyl.cut(groove)
