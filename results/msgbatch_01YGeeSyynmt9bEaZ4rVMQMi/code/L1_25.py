import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(20.0)
    .extrude(40.0)
    .faces(">Z").workplane()
    .cboreHole(10.0, 20.0, 10.0)
)
