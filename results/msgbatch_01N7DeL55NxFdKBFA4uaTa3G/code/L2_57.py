import cadquery as cq
import math

D = 100.0
H = 30.0
R = D / 2

# Main cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# 8 circular notches (r=10) centered on the outer edge
notch_pts = [(R * math.cos(math.radians(i * 45)), R * math.sin(math.radians(i * 45))) for i in range(8)]
notches = (
    cq.Workplane("XY")
    .pushPoints(notch_pts)
    .circle(10)
    .extrude(H)
)
body = body.cut(notches)

# Central bore D30 with 8x4 keyway
bore = cq.Workplane("XY").circle(15).extrude(H)
key = (
    cq.Workplane("XY")
    .center(16, 0)          # spans x 13..19 -> 4 mm beyond bore edge
    .rect(6, 8)
    .extrude(H)
)
body = body.cut(bore.union(key))

result = body
