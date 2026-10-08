import cadquery as cq

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

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
