import cadquery as cq
import math

# Ring: OD 80, ID 50, height 10
ring = cq.Workplane("XY").circle(40).circle(25).extrude(10)

# Single tooth triangle: P on outer circle, Q 5 mm radially outward, S back on the outer circle
ang = math.radians(-25)
P = (40, 0)
Q = (45, 0)
S = (40 * math.cos(ang), 40 * math.sin(ang))

tooth = (cq.Workplane("XY")
         .polyline([P, Q, S]).close()
         .extrude(10))

result = ring.union(tooth)

# Circular array: 12 teeth in total
for i in range(1, 12):
    t = tooth.rotate((0, 0, 0), (0, 0, 1), i * 30)
    result = result.union(t)
