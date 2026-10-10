import cadquery as cq
import math

R = 10.0
L = 50.0
groove_w = 5.0
depth = 9.0
r_neck = R - depth  # 1 mm radius -> 2 mm diameter

# Main cylinder along Z, from z=0 to z=50
base = cq.Workplane("XY").circle(R).extrude(L)

# Circumferential groove: annular ring cut in the middle
z0 = (L - groove_w) / 2.0
ring = (
    cq.Workplane("XY")
    .workplane(offset=z0)
    .circle(R + 1.0)
    .circle(r_neck)
    .extrude(groove_w)
)

result = base.cut(ring)
