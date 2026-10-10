import cadquery as cq

# Cylinder: diameter 40 mm, height 40 mm
cyl = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Conical pit profile on XZ plane (local x = X, local y = Z)
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 40.0), (15.0, 40.0), (0, 25.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(cone)
