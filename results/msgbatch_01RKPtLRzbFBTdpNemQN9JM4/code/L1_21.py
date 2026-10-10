import cadquery as cq

R = 25.0
H = 80.0
groove_w = 10.0
groove_d = 5.0

# Build via revolve of the profile around Z axis
r_in = R - groove_d
pts = [
    (0, 0),
    (R, 0),
    (R, H/2 - groove_w/2),
    (r_in, H/2 - groove_w/2),
    (r_in, H/2 + groove_w/2),
    (R, H/2 + groove_w/2),
    (R, H),
    (0, H),
]
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
