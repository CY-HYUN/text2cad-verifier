import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(30, 0), (0, 15), (-30, 0), (0, -15)])
    .close()
    .extrude(80)
)
