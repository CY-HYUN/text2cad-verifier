import cadquery as cq

# Profile in XZ plane: X = radius, Z = axial (local y of the XZ workplane)
# The "step" at Z=60 is degenerate (radius stays 20.0), so the section is a
# straight-walled hollow sleeve; the 3 mm fillet has no corner to act on.
pts = [
    (12.5, 0),
    (20.0, 0),
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
