import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(40, 40, 20, centered=(True, True, False))
    .faces(">Z").workplane()
    .circle(10).extrude(20)
)
