import cadquery as cq
import math

# Build frustum via revolve of profile (with chamfer at base outer edge, 2 mm x 45°)
R_bot = 35.0
R_top = 20.0
H = 60.0
r_hole = 10.0
c = 2.0

# Outer slanted side: from (35,0) to (20,60). Chamfer on base outer edge:
# bottom point moves inward by 2 along base: (33,0); vertical up 2 along the slanted wall to the point at z=2
# Chamfer 2 mm at 45°: from (R_bot - c, 0) to point on the slanted wall at height c
slope = (R_top - R_bot) / H  # dr/dz
r_at_c = R_bot + slope * c

pts = [
    (r_hole, 0),
    (R_bot - c, 0),
    (r_at_c, c),
    (R_top, H),
    (r_hole, H),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
