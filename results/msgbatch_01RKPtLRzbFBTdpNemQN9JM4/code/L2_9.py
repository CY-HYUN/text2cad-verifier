import cadquery as cq
import math

R = 40.0
Ri = 25.0
H = 10.0
th = 5.0
n = 12

ring = cq.Workplane("XY").circle(R).circle(Ri).extrude(H)

a = 2 * math.pi / n
p0 = (R, 0)
p1 = (R + th, 0)
p2 = (R * math.cos(a), R * math.sin(a))

# Slightly overlap into the ring for a robust union
p0b = (R - 1.0, 0)
p2b = ((R - 1.0) * math.cos(a), (R - 1.0) * math.sin(a))

tooth = (cq.Workplane("XY")
         .polyline([p0b, p1, p2, p2b]).close()
         .extrude(H))

result = ring
for i in range(n):
    result = result.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / n))
