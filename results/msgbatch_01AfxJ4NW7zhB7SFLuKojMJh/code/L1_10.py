import cadquery as cq

body = cq.Workplane("XY").box(100, 50, 30, centered=(True, True, False))
slot = (
    cq.Workplane("XY")
    .workplane(offset=15)
    .rect(100, 20)
    .extrude(15)
)
result = body.cut(slot)
