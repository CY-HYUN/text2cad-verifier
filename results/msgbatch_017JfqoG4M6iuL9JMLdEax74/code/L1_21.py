import cadquery as cq

# Main cylinder: Ø50 x 80, base on XY plane
body = cq.Workplane("XY").circle(25).extrude(80)

# Annular groove at mid-height: 10 wide, 5 deep
groove = (
    cq.Workplane("XY")
    .workplane(offset=40 - 5)
    .circle(25)
    .circle(20)
    .extrude(10)
)

result = body.cut(groove)
