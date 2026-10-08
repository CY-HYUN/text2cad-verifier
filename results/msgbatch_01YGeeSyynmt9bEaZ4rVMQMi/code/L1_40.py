import cadquery as cq

# Half-section profile in the XZ plane (x = radius, z = axial position)
pts = [
    (0, 0),
    (15, 0),
    (15, 20),
    (7.5, 20),
    (7.5, 40),
    (15, 40),
    (15, 60),
    (0, 60),
]

# Revolve 360 degrees about the Z axis
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
