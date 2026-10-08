import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(50)
    .extrude(10)
    .faces(">Z").workplane()
    .pushPoints([(35, 0), (-35, 0), (0, 35), (0, -35)])
    .hole(10)
)
