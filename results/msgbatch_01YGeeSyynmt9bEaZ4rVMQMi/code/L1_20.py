import cadquery as cq

# Trapezoidal side profile in the XZ plane (local x -> X, local y -> Z)
pts = [
    (0.0, 0.0),
    (80.0, 0.0),
    (80.0, 5.0),
    (0.0, 30.0),
]

# Plane "XZ" has normal -Y, so a negative extrude goes along +Y
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(-40.0)
)
