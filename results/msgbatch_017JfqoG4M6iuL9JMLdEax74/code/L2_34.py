import cadquery as cq

# Main cylinder: diameter 20 mm, length 50 mm, axis along Z
L = 50.0
R = 10.0
groove_w = 5.0
groove_depth = 9.0
core_r = R - groove_depth  # 1 mm radius -> 2 mm remaining neck diameter

body = cq.Workplane("XY").circle(R).extrude(L)

# Circumferential groove centred at mid-length: remove an annulus
z0 = L / 2 - groove_w / 2
groove = (
    cq.Workplane("XY")
    .workplane(offset=z0)
    .circle(R + 1.0)
    .circle(core_r)
    .extrude(groove_w)
)

result = body.cut(groove)
