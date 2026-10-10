import cadquery as cq
import math

# Outer solid: straight edge height 50, quarter ellipse 100 x 50
outer = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(100, 0)
    .lineTo(100, 50)
    .ellipseArc(100, 50, 0, 90, startAtCurrent=True)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Inner solid: offset inward by 10 mm
inner = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(90, 0)
    .lineTo(90, 50)
    .ellipseArc(90, 40, 0, 90, startAtCurrent=True)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

head = outer.cut(inner)

# Nozzle ring on the tangent plane at the top vertex (y = 100), extruded outward (+Y) 30 mm
nozzle = (
    cq.Workplane("XZ", origin=(0, 100, 0))
    .circle(20)
    .circle(15)
    .extrude(-30)
)

result = head.union(nozzle)
