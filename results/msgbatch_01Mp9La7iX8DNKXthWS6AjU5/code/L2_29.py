import cadquery as cq
import math

ring = cq.Workplane("XY").circle(50).circle(30).extrude(20)

# single tooth: radial from 27 to 30.5 (slight overlap into ring), 5 wide, 20 tall
tooth = (cq.Workplane("XY")
         .center(28.75, 0)
         .rect(3.5, 5)
         .extrude(20))

result = ring
for i in range(12):
    t = tooth.rotate((0, 0, 0), (0, 0, 1), i * 30)
    result = result.union(t)
