import cadquery as cq
import math

# Outer solid profile (XZ plane: local x = world X, local y = world Z)
outer = (
    cq.Workplane("XZ")
    .moveTo(0, -25)
    .lineTo(100, -25)
    .lineTo(100, 0)
    .ellipseArc(100, 50, 0, 90)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Inner (offset 8 mm) solid profile
inner = (
    cq.Workplane("XZ")
    .moveTo(0, -30)
    .lineTo(92, -30)
    .lineTo(92, 0)
    .ellipseArc(92, 42, 0, 90)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

shell = outer.cut(inner)

# Top nozzle: tangent plane at apex (z = 50), concentric circles 40 / 30, extrude 30
nozzle = (
    cq.Workplane("XY")
    .workplane(offset=50)
    .circle(20)
    .circle(15)
    .extrude(30)
)

result = shell.union(nozzle)
