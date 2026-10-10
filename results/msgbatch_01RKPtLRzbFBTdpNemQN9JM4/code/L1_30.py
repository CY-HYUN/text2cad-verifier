import cadquery as cq

# Main cylinder: diameter 30, height 60, axis along Z (base at z=0)
body = cq.Workplane("XY").circle(15).extrude(60)

# Transverse through-hole along Y at mid-height, diameter 10
hole = (
    cq.Workplane("XZ")
    .workplane(offset=-20)
    .center(0, 30)
    .circle(5)
    .extrude(40)
)

result = body.cut(hole)
