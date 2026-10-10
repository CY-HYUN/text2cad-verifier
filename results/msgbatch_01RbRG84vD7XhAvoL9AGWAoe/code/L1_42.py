import cadquery as cq
import math

D = 30.0
H = 50.0
ang = 30.0

cyl = cq.Workplane("XY").circle(D / 2).extrude(H)

# Cutting half-space: big box above a plane tilted 30 deg, passing through (-R, 0, H)
cutter = (
    cq.Workplane("XY")
    .box(300, 300, 300)
    .translate((0, 0, 150))
    .rotate((0, 0, 0), (0, 1, 0), ang)
    .translate((-D / 2, 0, H))
)

result = cyl.cut(cutter)
