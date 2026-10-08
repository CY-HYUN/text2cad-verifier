import cadquery as cq
import math

D = 100.0
T = 30.0
R = D / 2
groove_r = 10.0
n_grooves = 8
hole_d = 30.0
key_w = 8.0
key_depth = 4.0

# Main disc
body = cq.Workplane("XY").circle(R).extrude(T)

# Semicircular grooves centered on the outer circumference
pts = [(R * math.cos(2 * math.pi * i / n_grooves),
        R * math.sin(2 * math.pi * i / n_grooves)) for i in range(n_grooves)]
grooves = (cq.Workplane("XY").pushPoints(pts).circle(groove_r)
           .extrude(T + 2).translate((0, 0, -1)))
body = body.cut(grooves)

# Central bore
bore = (cq.Workplane("XY").circle(hole_d / 2).extrude(T + 2)
        .translate((0, 0, -1)))
body = body.cut(bore)

# Keyway: 8 mm wide, extends 4 mm beyond the bore wall in +X
key_len = hole_d / 2 + key_depth
key = (cq.Workplane("XY")
       .center(key_len / 2, 0)
       .rect(key_len, key_w)
       .extrude(T + 2)
       .translate((0, 0, -1)))
body = body.cut(key)

result = body
