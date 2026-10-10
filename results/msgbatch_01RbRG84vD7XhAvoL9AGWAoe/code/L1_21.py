import cadquery as cq

D = 50.0
H = 80.0
groove_w = 10.0
groove_d = 5.0

body = cq.Workplane("XY").circle(D / 2).extrude(H)

# Annular groove centered at mid-height
groove = (
    cq.Workplane("XY")
    .workplane(offset=H / 2 - groove_w / 2)
    .circle(D / 2 + 1)
    .circle(D / 2 - groove_d)
    .extrude(groove_w)
)

result = body.cut(groove)
