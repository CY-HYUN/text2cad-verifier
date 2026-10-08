import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(45.0)
    .extrude(15.0)
    .faces(">Z").workplane()
    .rect(30.0, 30.0)
    .cutThruAll()
)
