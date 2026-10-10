import cadquery as cq

block = cq.Workplane("XY").rect(90.0, 50.0).extrude(30.0)

groove = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(90.0, 20.0)
    .extrude(-12.0)
)

cut = block.cut(groove)

result = cut.edges(
    cq.selectors.BoxSelector((-46, -11, 17.5), (46, 11, 18.5))
).edges("|X").fillet(2.0)
