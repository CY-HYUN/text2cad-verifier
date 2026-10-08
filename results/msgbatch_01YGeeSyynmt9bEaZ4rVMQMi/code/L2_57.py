import cadquery as cq
import math

D = 100.0
H = 30.0
R = D / 2

# Base cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# Eight notches: R10 circles centred on the outer edge
pts = [(R * math.cos(math.radians(i * 45)), R * math.sin(math.radians(i * 45))) for i in range(8)]
notches = cq.Workplane("XY").pushPoints(pts).circle(10).extrude(H)
body = body.cut(notches)

# Central bore D30 with an 8 mm wide keyway reaching 4 mm past the bore
bore = cq.Workplane("XY").circle(15).extrude(H)
key = cq.Workplane("XY").center(0, 15).rect(8, 8).extrude(H)  # spans y = 11..19
body = body.cut(bore.union(key))

result = body
