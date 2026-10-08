import cadquery as cq

pts = [(0, 0), (80.0, 0), (80.0, 5.0), (0, 30.0)]
result = cq.Workplane("XZ").polyline(pts).close().extrude(-40.0)
