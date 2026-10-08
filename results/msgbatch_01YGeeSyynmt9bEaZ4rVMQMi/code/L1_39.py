import cadquery as cq

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(60, 0)
    .threePointArc((80, 20), (60, 40))
    .lineTo(0, 40)
    .close()
    .extrude(10.0)
)
