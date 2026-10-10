import cadquery as cq
import math

R_bot = 35.0
R_top = 20.0
H = 60.0
r_hole = 10.0
c = 2.0

# direction along slanted outer face (from bottom edge upward)
L = math.hypot(R_bot - R_top, H)
dr = -(R_bot - R_top) / L * c
dz = H / L * c

pts = [
    (r_hole, 0),
    (R_bot - c, 0),
    (R_bot + dr, dz),
    (R_top, H),
    (r_hole, H),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
