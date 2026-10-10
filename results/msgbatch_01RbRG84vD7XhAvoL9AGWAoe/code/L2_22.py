import cadquery as cq

L = 40.0
hole_d = 30.0
ch = 10.0

result = (
    cq.Workplane("XY")
    .box(L, L, L)
    .edges("|Z")
    .chamfer(ch)
    .faces(">Z")
    .workplane()
    .hole(hole_d)
)
