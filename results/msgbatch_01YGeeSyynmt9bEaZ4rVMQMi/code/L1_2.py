import cadquery as cq

# Section in XZ plane: local x = radius, local y = axial (global Z)
pts = [
    (12.5, 0.0),
    (20.0, 0.0),
    (20.0, 60.0),
    (20.0, 120.0),
    (12.5, 120.0),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
