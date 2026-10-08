import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(40, 40, 40)
    .edges("|Z")
    .chamfer(10)
    .faces(">Z")
    .workplane()
    .hole(30)
)
