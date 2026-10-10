import cadquery as cq

blank = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

notch = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .center(-10 + 25, 15)
    .rect(50.0, 30.0)
    .extrude(-20.0)
)

body = blank.cut(notch)

result = body.edges(
    cq.selectors.BoxSelector((-10.5, -0.5, 9.0), (-9.5, 0.5, 31.0))
).fillet(4.0)
