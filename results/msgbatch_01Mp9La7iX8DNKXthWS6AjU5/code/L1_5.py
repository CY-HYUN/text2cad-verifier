import cadquery as cq
import math

# Square base 60x60, extruded 10 mm (centered on origin in XY)
base = cq.Workplane("XY").rect(60.0, 60.0).extrude(10.0)

# Cylindrical pillar, diameter 30, height 50, on top of base center
pillar = (
    cq.Workplane("XY")
    .workplane(offset=10.0)
    .circle(15.0)
    .extrude(50.0)
)

result = base.union(pillar)
