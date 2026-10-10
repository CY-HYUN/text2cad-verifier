import math
import cadquery as cq

R = 15.0
H_total = 50.0
ang = 30.0
h = H_total - R * math.tan(math.radians(ang))

cyl = cq.Workplane("XY").circle(R).extrude(80)

cutter = (
    cq.Workplane("XY")
    .box(200, 200, 200, centered=(True, True, False))
    .rotate((0, 0, 0), (0, 1, 0), -ang)
    .translate((0, 0, h))
)

result = cyl.cut(cutter)
