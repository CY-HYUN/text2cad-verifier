import cadquery as cq

pts = [(10.0, 0.0), (35.0, 0.0), (20.0, 60.0), (10.0, 60.0)]
body = (
    cq.Workplane("XZ")
    .polyline(pts).close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = (
    body.faces("<Z")
    .edges(cq.selectors.RadiusNthSelector(1))
    .chamfer(2.0)
)
