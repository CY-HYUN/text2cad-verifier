import cadquery as cq

cyl = cq.Workplane("XY").circle(25.0).extrude(20.0)

cone = (
    cq.Workplane("XZ")
    .polyline([(0, 20), (25, 20), (0, 60)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.union(cone)
