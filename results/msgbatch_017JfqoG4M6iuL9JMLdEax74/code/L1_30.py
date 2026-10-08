import cadquery as cq

# Main body: solid cylinder, diameter 30 mm, height 60 mm, axis along Z
body = cq.Workplane("XY").circle(15).extrude(60)

# Transverse pin hole: diameter 10 mm, along Y, at mid-height (z = 30)
hole = (
    cq.Workplane("XZ")
    .workplane(offset=-20)
    .center(0, 30)
    .circle(5)
    .extrude(40)
)

result = body.cut(hole)
