import cadquery as cq
import math

# Outer sloped column: front (y=-30) height 60, rear (y=+30) height 100
profile = [(-30, 0), (30, 0), (30, 100), (-30, 60)]
outer = (
    cq.Workplane("YZ")
    .polyline(profile).close()
    .extrude(30, both=True)  # 60 mm in X
)

# Hollow interior, 5 mm walls, open top and bottom
inner = cq.Workplane("XY").box(50, 50, 400)
shell = outer.cut(inner)

# 20 mm hole through the rear (taller) wall
hole = (
    cq.Workplane("XZ", origin=(0, 30, 0))
    .center(0, 75)
    .circle(10)
    .extrude(20, both=True)
)

result = shell.cut(hole)
