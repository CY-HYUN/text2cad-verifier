import cadquery as cq

# Cylinder: diameter 50 mm, height 80 mm along +Z
cyl = cq.Workplane("XY").circle(25.0).extrude(80.0)

# Annular groove: 5 mm deep radially (r = 20..25), 10 mm wide axially, centred at z = 40
# Rectangle on XZ plane, revolved 360 degrees about the Z axis
groove = (
    cq.Workplane("XZ")
    .polyline([(20.0, 35.0), (25.5, 35.0), (25.5, 45.0), (20.0, 45.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(groove)
