import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(120.0, 40.0)
    .extrude(10.0)
    .faces(">Z")
    .workplane()
    .pushPoints([(-40.0, 0), (40.0, 0)])
    .hole(10.0)
)
