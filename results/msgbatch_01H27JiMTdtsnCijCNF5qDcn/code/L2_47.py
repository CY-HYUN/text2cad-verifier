import cadquery as cq

ri = 20.0   # inner radius
ro = 25.0   # outer radius (wall thickness 5)
L = 100.0   # tube length

pts = [
    (ri, 0), (ro + 10, 0), (ro + 10, 5), (ro, 5),
    (ro, L/2 - 2.5), (ro + 5, L/2 - 2.5), (ro + 5, L/2 + 2.5), (ro, L/2 + 2.5),
    (ro, L - 5), (ro + 10, L - 5), (ro + 10, L), (ri, L),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
