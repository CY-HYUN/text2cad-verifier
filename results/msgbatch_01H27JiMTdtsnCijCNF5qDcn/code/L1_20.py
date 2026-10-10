import cadquery as cq

pts = [(0, 0), (80, 0), (80, 5), (0, 30)]
result = cq.Workplane("XZ").polyline(pts).close().extrude(-40.0)
