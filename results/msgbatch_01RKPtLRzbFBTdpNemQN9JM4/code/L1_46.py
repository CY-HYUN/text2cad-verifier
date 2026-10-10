import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (30, 0), (0, 40)])
    .close()
    .extrude(60)
)
