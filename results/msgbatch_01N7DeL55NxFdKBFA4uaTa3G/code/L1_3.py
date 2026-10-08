import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(50.0, 50.0)
    .extrude(50.0)
    .faces(">Z").workplane()
    .circle(10.0)
    .cutThruAll()
)
