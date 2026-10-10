import cadquery as cq

R = 25.0
H = 80.0
groove_w = 10.0
groove_d = 5.0

# Cylinder centered on origin in XY, extending from z=0 to z=H
body = cq.Workplane("XY").circle(R).extrude(H)

# Annular groove: ring between R-groove_d and R (plus margin), centered at mid-height
ring = (
    cq.Workplane("XY")
    .workplane(offset=H / 2 - groove_w / 2)
    .circle(R + 1)
    .circle(R - groove_d)
    .extrude(groove_w)
)

result = body.cut(ring)
