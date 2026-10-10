import cadquery as cq

result = (
    cq.Workplane("YZ")
    .moveTo(-30, 0)
    .lineTo(-20, 0)
    .threePointArc((0, 20), (20, 0))
    .lineTo(30, 0)
    .threePointArc((0, 30), (-30, 0))
    .close()
    .extrude(100.0)
)
