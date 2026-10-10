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

# Semicircular grooves centred on the outer circumference
for i in range(n_grooves):
    a = 2 * math.pi * i / n_grooves
    x, y = R * math.cos(a), R * math.sin(a)
    cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(groove_r)
        .extrude(T)
    )
    body = body.cut(cutter)

# Central hole
body = body.cut(cq.Workplane("XY").circle(hole_d / 2).extrude(T))

# Keyway in the hole wall (+X direction)
key_len = hole_d / 2 + key_depth
keyway = (
    cq.Workplane("XY")
    .center(key_len / 2, 0)
    .rect(key_len, key_w)
    .extrude(T)
)
body = body.cut(keyway)

result = body
