import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 50, 50)
    .faces(">Z")
    .workplane()
    .hole(20)
)
