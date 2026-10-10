import cadquery as cq
import math

# Revolved profile: outer cone, with a 2mm 45° chamfer at the base outer edge, through-hole of dia 20
R_bot = 35.0
R_top = 20.0
H = 60.0
r_hole = 10.0
c = 2.0

# Outer cone slope: radius shrinks 15 over 60 height.
# Chamfer on base outer edge: 45° chamfer with 2mm width -> bottom edge moved inward by 2 and up by 2
# Intersect chamfer line with cone: build chamfer by cutting with a revolved triangle-based approach.

pts = [
    (r_hole, 0),
    (R_bot - c, 0),
    (R_bot, c),
]
# point on the cone at z=c
r_at_c = R_bot - (R_bot - R_top) * c / H
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
