import cadquery as cq
import math

# Base cylinder: diameter 100, height 30
result = cq.Workplane("XY").circle(50).extrude(30)

# 8 circular cuts of radius 10 centered on the cylinder edge (radius 50)
pts = [(50 * math.cos(math.radians(i * 45)), 50 * math.sin(math.radians(i * 45))) for i in range(8)]
cutters = (
    cq.Workplane("XY")
    .pushPoints(pts)
    .circle(10)
    .extrude(30)
)
result = result.cut(cutters)

# Central bore diameter 30 with keyway 8 x 4 (width 8, extends 4 beyond bore)
bore = cq.Workplane("XY").circle(15).extrude(30)
# keyway: width 8 (Y), depth 4 beyond the bore radius, overlapping the bore for connection
key = (
    cq.Workplane("XY")
    .center((15 + 4 - 0) / 2 + 0, 0)
    .rect(19, 8)
    .extrude(30)
)
result = result.cut(bore).cut(key)
