import cadquery as cq

# Half-section on XZ plane (local x -> X, local y -> Z)
pts = [(10.0, 0.0), (35.0, 0.0), (20.0, 60.0), (10.0, 60.0)]

body = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# 45° chamfer, distance 2.0, on the outer bottom edge (radius 35)
result = (
    body.faces("<Z")
    .edges(cq.selectors.RadiusNthSelector(1))
    .chamfer(2.0)
)
