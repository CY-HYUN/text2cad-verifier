import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(20).extrude(40)
    .faces(">Z").workplane()
    .cboreHole(10, 20, 10)
)
