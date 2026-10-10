import cadquery as cq

# 40 mm cube centered in XY, Z from 0 to 40
body = cq.Workplane("XY").box(40, 40, 40, centered=(True, True, False))

# Through-hole, diameter 20
through = cq.Workplane("XY").circle(10).extrude(40)

# Counterbore from top, diameter 30, depth 10
cbore = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .circle(15)
    .extrude(10)
)

result = body.cut(through).cut(cbore)
