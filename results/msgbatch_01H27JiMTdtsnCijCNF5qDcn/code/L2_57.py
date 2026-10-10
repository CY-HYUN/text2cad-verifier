import cadquery as cq
import math

# Base cylinder: diameter 100, height 30
result = cq.Workplane("XY").circle(50).extrude(30)

# 8 circular cuts of radius 10, centered on the cylinder's outer edge
for i in range(8):
    a = math.radians(i * 45)
    x = 50 * math.cos(a)
    y = 50 * math.sin(a)
    cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(10)
        .extrude(30)
    )
    result = result.cut(cutter)

# Central bore diameter 30 with keyway 8 wide x 4 deep (beyond the bore)
bore = cq.Workplane("XY").circle(15).extrude(30)
# Keyway: width 8 (Y), extends 4 mm beyond bore radius in +X
key = (
    cq.Workplane("XY")
    .center((15 + 4 + 0) / 2 - 2, 0)
    .rect(19 - 0, 8)
    .extrude(30)
)
# Rectangle spans x from 0 to 19 (overlaps bore, protrudes 4 mm)
key = cq.Workplane("XY").center(9.5, 0).rect(19, 8).extrude(30)

result = result.cut(bore).cut(key)
