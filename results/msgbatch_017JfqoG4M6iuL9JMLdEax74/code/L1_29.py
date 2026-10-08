import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(30).extrude(10)
    .faces(">Z").workplane().circle(20).extrude(10)
    .faces(">Z").workplane().circle(10).extrude(10)
)
