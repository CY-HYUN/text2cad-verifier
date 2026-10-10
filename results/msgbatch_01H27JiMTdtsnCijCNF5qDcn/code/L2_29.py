import cadquery as cq
import math

ring = (cq.Workplane("XY").circle(50).circle(30).extrude(20))

result = ring
for i in range(12):
    tooth = (cq.Workplane("XY")
             .center(29, 0)
             .rect(4, 5)
             .extrude(20)
             .rotate((0, 0, 0), (0, 0, 1), i * 30))
    result = result.union(tooth)
