import math
import cadquery as cq

R = 15.0
H = 50.0
ang = 30.0
h0 = H - R * math.tan(math.radians(ang))  # height at axis

cyl = cq.Workplane("XY").circle(R).extrude(H + 20)

big = 200.0
box = (cq.Workplane("XY")
       .box(big, big, big, centered=(True, True, False))
       .rotate((0, 0, 0), (0, 1, 0), ang)
       .translate((0, 0, h0)))

result = cyl.cut(box)
