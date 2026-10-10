import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(20)
    .cut(cq.Workplane("XY").center(10, 0).circle(20).extrude(20))
)
