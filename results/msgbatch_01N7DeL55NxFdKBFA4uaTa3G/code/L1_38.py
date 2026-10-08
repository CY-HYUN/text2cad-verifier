import cadquery as cq

# Rhombus in the XY plane: diagonals cross at the origin,
# long diagonal (60 mm) along X, short diagonal (30 mm) along Y
long_d = 60.0
short_d = 30.0
height = 80.0

pts = [
    (long_d / 2, 0),
    (0, short_d / 2),
    (-long_d / 2, 0),
    (0, -short_d / 2),
]

# Extrude 80 mm along +Z to form the rhombic prism
result = cq.Workplane("XY").polyline(pts).close().extrude(height)
