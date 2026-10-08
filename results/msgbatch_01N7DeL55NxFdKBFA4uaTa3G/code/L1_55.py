import cadquery as cq

# Half cross-section in the XZ plane (local x = radius, local y = global Z)
profile = (
    cq.Workplane("XZ")
    .polyline([(10.0, 0.0), (35.0, 0.0), (20.0, 60.0), (10.0, 60.0)])
    .close()
)

# Revolve 360 degrees around the global Z axis (local y axis)
body = profile.revolve(360.0, (0, 0, 0), (0, 1, 0))

# Chamfer the outer edge of the bottom face (radius 35)
result = (
    body.faces("<Z")
    .edges(cq.selectors.RadiusNthSelector(1))
    .chamfer(2.0)
)
