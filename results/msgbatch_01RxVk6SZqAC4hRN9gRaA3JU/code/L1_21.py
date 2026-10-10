import cadquery as cq

cyl = cq.Workplane("XY").circle(25.0).extrude(80.0)

# Groove ring: outer radius 25 (slightly beyond), inner radius 20, z from 35 to 45
groove = (
    cq.Workplane("XY")
    .workplane(offset=35.0)
    .circle(26.0)
    .circle(20.0)
    .extrude(10.0)
)

result = cyl.cut(groove)
