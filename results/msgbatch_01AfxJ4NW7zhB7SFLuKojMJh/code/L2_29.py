import cadquery as cq
import math

ring = cq.Workplane("XY").circle(50).circle(30).extrude(20)

teeth = None
for i in range(12):
    t = (cq.Workplane("XY")
         .center(28, 0)
         .rect(6, 5)
         .extrude(20)
         .rotate((0, 0, 0), (0, 0, 1), i * 30))
    teeth = t if teeth is None else teeth.union(t)

result = ring.union(teeth)
