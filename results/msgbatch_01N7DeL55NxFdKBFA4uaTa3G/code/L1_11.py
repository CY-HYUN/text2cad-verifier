import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(30.0)
    .extrude(40.0)
    .faces(">Z")
    .workplane()
    .center(15.0, 0)
    .circle(5.0)
    .cutThruAll()
)
