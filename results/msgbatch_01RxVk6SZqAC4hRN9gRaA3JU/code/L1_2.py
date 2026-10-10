import cadquery as cq

# Hollow sleeve section in XZ plane: X = radius, Z = axial
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
