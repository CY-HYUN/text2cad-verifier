import cadquery as cq
import math

# Cylinder: diameter 30 mm, height 50 mm
cyl = cq.Workplane("XY").circle(15.0).extrude(50.0)

# Cutting plane through (-15, 0, 50), tilted 30 deg about the Y axis.
# Plane: z = 50 - tan(30)*(x + 15); it drops 17.32 mm across the diameter.
# A large box above the plane is used as the material to remove.
angle = 30.0
cutter = (
    cq.Workplane("XY")
    .box(300, 300, 300)
    .translate((0, 0, 150))                      # bottom face on z=0
    .rotate((0, 0, 0), (0, 1, 0), angle)         # normal -> (sin30, 0, cos30)
    .translate((-15.0, 0, 50.0))                 # pass through edge point
)

result = cyl.cut(cutter)
