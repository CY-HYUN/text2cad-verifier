import cadquery as cq

# Main cube body 40x40x40, centered in XY, base at z=0
body = cq.Workplane("XY").box(40, 40, 40, centered=(True, True, False))

# Through-hole, diameter 20
body = body.faces(">Z").workplane().hole(20)

# Counterbore from top, diameter 30, depth 10
cbore = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .circle(15)
    .extrude(10)
)
result = body.cut(cbore)
