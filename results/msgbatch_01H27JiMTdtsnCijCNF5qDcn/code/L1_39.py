import cadquery as cq

result = (
    cq.Workplane("XY")
    .moveTo(0, -20)
    .lineTo(60, -20)
    .threePointArc((80, 0), (60, 20))
    .lineTo(0, 20)
    .close()
    .extrude(10.0)
)
