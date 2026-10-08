import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(50.0)
    .extrude(5.0)
    .faces(">Z").workplane()
    .hole(50.0)
)
