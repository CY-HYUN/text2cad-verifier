import cadquery as cq
import math

# Base cylinder: diameter 30 mm, height 50 mm
cyl = cq.Workplane("XY").circle(15.0).extrude(50.0)

# Inclined cutting plane through (-15, 0, 50), tilted 30 deg about Y,
# descending toward +X (drop of 30*tan30 = 17.32 mm across the diameter)
angle = 30.0
cutter = (
    cq.Workplane("XY")
    .box(300, 300, 300, centered=(True, True, False))  # bottom face on z=0, extends upward
    .rotate((0, 0, 0), (0, 1, 0), angle)
    .translate((-15.0, 0, 50.0))
)

result = cyl.cut(cutter)
