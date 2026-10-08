import cadquery as cq

# Cylinder base: diameter 50, height 20
cyl = cq.Workplane("XY").circle(25.0).extrude(20.0)

# Cone profile on XZ plane: right triangle, base radius 25, height 40, sitting on top of cylinder
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 20.0), (25.0, 20.0), (0, 60.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))  # local Y of XZ plane = global Z axis
)

result = cyl.union(cone)
