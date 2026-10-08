import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(120, 40, 10)
    .faces(">Z").workplane()
    .pushPoints([(-40, 0), (40, 0)])
    .hole(10)
)
