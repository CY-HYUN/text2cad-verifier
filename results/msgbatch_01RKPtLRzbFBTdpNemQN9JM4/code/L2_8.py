import cadquery as cq
import math

R = 50.0
T = 5.0
ang = 30.0
n = 10

column = cq.Workplane("XY").circle(10).extrude(100)

result = column
for i in range(n):
    a0 = 0.0
    a1 = math.radians(ang)
    am = a1 / 2
    step = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(R, 0)
        .threePointArc((R * math.cos(am), R * math.sin(am)), (R * math.cos(a1), R * math.sin(a1)))
        .close()
        .extrude(T)
        .rotate((0, 0, 0), (0, 0, 1), ang * i)
        .translate((0, 0, 10 * i))
    )
    result = result.union(step)
