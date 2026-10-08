import cadquery as cq

# Cylinder: diameter 50 mm, height 20 mm, base on the XY plane
cylinder = cq.Workplane("XY").circle(25.0).extrude(20.0)

# Cone: right-triangle profile drawn on the XZ plane (local y = global Z),
# base radius 25 mm, height 40 mm, sitting on top of the cylinder (z = 20)
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 20.0), (25.0, 20.0), (0, 60.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))  # revolve about global Z axis
)

result = cylinder.union(cone)
