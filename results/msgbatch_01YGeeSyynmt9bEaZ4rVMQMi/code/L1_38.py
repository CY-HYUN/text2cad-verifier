import cadquery as cq

# Rhombus with diagonals 60 mm (along X) and 30 mm (along Y), centred on the origin
long_diag = 60.0
short_diag = 30.0
height = 80.0

pts = [
    (long_diag / 2, 0),
    (0, short_diag / 2),
    (-long_diag / 2, 0),
    (0, -short_diag / 2),
]

result = cq.Workplane("XY").polyline(pts).close().extrude(height)
