import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(120.0, 40.0, 10.0, centered=(True, True, False))
    .faces(">Z").workplane()
    .pushPoints([(-40.0, 0.0), (40.0, 0.0)])
    .hole(10.0)
)
