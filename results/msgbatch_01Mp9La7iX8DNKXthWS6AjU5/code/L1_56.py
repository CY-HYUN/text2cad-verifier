import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(80, 80)
    .workplane(offset=45)
    .rect(50, 50)
    .loft(combine=True)
)

result = (
    result.faces(">Z").workplane()
    .rect(30, 30)
    .cutBlind(-15)
)

result = result.faces(">Z").edges("not %LINE or %LINE").edges(
    cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46))
).chamfer(1.0)
