import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(120, 50, 6, centered=(True, True, False))
    .edges("|Z").fillet(4)
    .faces(">Z").workplane()
    .slot2D(80, 18, 0)
    .cutThruAll()
)
