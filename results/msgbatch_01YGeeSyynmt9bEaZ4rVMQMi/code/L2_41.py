import cadquery as cq
import math

R = 20.0          # circumscribed radius
H = 60.0          # extrusion height
r_in = R * math.cos(math.pi / 8)  # inscribed radius (flat-to-center)

# Octagonal prism
body = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# Triangular profile at the top corner (45 deg), revolved around central axis -> sharpened tip
tri = (
    cq.Workplane("XZ")
    .polyline([(0, H), (R + 2, H), (R + 2, H - (R + 2))])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(tri)

# Annular groove at mid height: 5 mm wide, 2 mm deep from the flat faces
gw = 5.0
gd = 2.0
zc = H / 2
groove = (
    cq.Workplane("XZ")
    .polyline([
        (r_in - gd, zc - gw / 2),
        (R + 2, zc - gw / 2),
        (R + 2, zc + gw / 2),
        (r_in - gd, zc + gw / 2),
    ])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(groove)

result = body
