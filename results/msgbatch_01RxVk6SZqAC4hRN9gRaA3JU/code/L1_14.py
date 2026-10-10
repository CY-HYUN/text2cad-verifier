import cadquery as cq

# Cylinder base: diameter 50, height 20
cylinder = cq.Workplane("XY").circle(25.0).extrude(20.0)

# Cone: right triangle profile on XZ plane, revolved 360° about Z axis
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 20.0), (25.0, 20.0), (0, 60.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cylinder.union(cone)
