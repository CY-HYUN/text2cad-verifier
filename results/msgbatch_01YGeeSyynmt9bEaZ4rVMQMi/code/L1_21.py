import cadquery as cq

# Base cylinder: diameter 50 mm, height 80 mm, standing on the XY plane
cyl = cq.Workplane("XY").circle(25.0).extrude(80.0)

# Groove profile on the XZ plane: radial depth 5 mm, axial width 10 mm,
# centred at z = 40 mm. Its outer edge sits slightly beyond the cylinder surface.
groove = (
    cq.Workplane("XZ")
    .moveTo(20.0, 35.0)
    .lineTo(26.0, 35.0)
    .lineTo(26.0, 45.0)
    .lineTo(20.0, 45.0)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(groove)
