import cadquery as cq

# Base cylinder: diameter 40 mm, height 40 mm, standing on the XY plane
cyl = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Triangular profile on the XZ plane (local x = global X, local y = global Z)
# Top radius 15 mm at z = 40, apex 15 mm deep at z = 25
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 40.0), (15.0, 40.0), (0, 25.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))  # revolve around global Z axis
)

result = cyl.cut(cone)
