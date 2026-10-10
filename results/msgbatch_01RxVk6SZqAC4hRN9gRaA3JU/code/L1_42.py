import cadquery as cq
import math

# Base cylinder: diameter 30 mm, height 50 mm
radius = 15.0
height = 50.0
cyl = cq.Workplane("XY").circle(radius).extrude(height)

# Inclined cutting plane through (-15, 0, 50), tilted 30 deg about Y
# (slopes downward toward +X: z = 50 - (x + 15) * tan(30))
angle = 30.0
cutter = (
    cq.Workplane("XY")
    .box(200, 200, 200, centered=(True, True, False))  # bottom face on local z=0
    .rotate((0, 0, 0), (0, 1, 0), angle)
    .translate((-radius, 0, height))
)

result = cyl.cut(cutter)
