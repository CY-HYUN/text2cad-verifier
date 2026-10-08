import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(120.0, 50.0)
    .extrude(6.0)
    .edges("|Z").fillet(4.0)
    .faces(">Z").workplane()
    .slot2D(80.0, 18.0, 0)
    .cutThruAll()
)
