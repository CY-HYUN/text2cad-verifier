import cadquery as cq

# Rhombus with diagonals 60 (X) and 30 (Y), extruded 80 along Z
pts = [(30, 0), (0, 15), (-30, 0), (0, -15)]
result = cq.Workplane("XY").polyline(pts).close().extrude(80)
