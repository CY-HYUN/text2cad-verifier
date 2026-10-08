import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(50.0)
    .extrude(10.0)
    .faces(">Z").workplane()
    .polarArray(35.0, 0, 360, 4)
    .circle(5.0)
    .cutThruAll()
)
