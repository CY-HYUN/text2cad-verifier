import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(40, 40, 40)
    .faces(">Z").workplane()
    .cboreHole(20, 30, 10)
)
