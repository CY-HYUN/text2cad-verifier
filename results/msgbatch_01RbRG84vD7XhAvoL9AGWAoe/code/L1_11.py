import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(30)
    .extrude(40)
    .faces(">Z").workplane()
    .center(15, 0)
    .hole(10)
)
