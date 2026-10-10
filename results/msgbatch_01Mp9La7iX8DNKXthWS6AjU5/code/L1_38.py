import cadquery as cq

# Rhombus with diagonals 60 (along X) and 30 (along Y), centered at the origin
pts = [(30, 0), (0, 15), (-30, 0), (0, -15)]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(80.0)
)
