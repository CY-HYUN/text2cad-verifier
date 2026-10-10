import cadquery as cq
import math

# Cylinder: diameter 50, height 80
cyl = cq.Workplane("XY").circle(25.0).extrude(80.0)

# Groove cross-section on XZ plane: radial from r=20 to r=25 (outer edge at cylinder surface),
# axial from z=35 to z=45 (centered at z=40)
# On XZ plane, local x = global X, local y = global Z
groove = (
    cq.Workplane("XZ")
    .moveTo(20.0, 35.0)
    .lineTo(25.0, 35.0)
    .lineTo(25.0, 45.0)
    .lineTo(20.0, 45.0)
    .close()
    .revolve(360.0, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(groove)
