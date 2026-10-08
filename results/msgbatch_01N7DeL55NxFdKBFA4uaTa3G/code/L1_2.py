import cadquery as cq

# The profile's inward step at Z=60 has zero width (20.0 -> 20.0), so the
# 3 mm fillet has no corner to round. The section reduces to a rectangle.
pts = [
    (12.5, 0.0),
    (20.0, 0.0),
    (20.0, 60.0),
    (20.0, 120.0),
    (12.5, 120.0),
]

# Sketch on the XZ plane (local x = radius, local y = Z axial), revolve 360° about Z
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
