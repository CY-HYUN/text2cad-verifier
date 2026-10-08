import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(40.0)
    .extrude(20.0)
    .faces(">Z").workplane()
    .circle(20.0)
    .extrude(30.0)
)
