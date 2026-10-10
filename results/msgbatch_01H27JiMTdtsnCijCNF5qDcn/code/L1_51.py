import cadquery as cq
import math

# Base disc: diameter 60, thickness 10
disc = cq.Workplane("XY").circle(30.0).extrude(10.0)

# Cutout circle: diameter 60, centered on the edge of the disc at (30, 0), cut through full thickness
cutter = (
    cq.Workplane("XY")
    .workplane(offset=10.0)
    .center(30.0, 0)
    .circle(30.0)
    .extrude(-10.0)
)

result = disc.cut(cutter)
