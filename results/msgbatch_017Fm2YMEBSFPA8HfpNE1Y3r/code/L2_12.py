import cadquery as cq
import math

# Create the base: stretch a 100mm diameter circle to 10mm thick
base = cq.Workplane("XY").circle(50).extrude(10)

# Create a single frustum using loft
# Bottom profile: 20mm diameter (radius 10mm) at height 10mm (top of base)
# Top profile: 10mm diameter (radius 5mm) at height 25mm (15mm above base top)
frustum = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(10)
    .workplane(offset=15)
    .circle(5)
    .loft()
)

# Combine base with the frustum
result = base.union(frustum)

# Create circular array of frustums (3 times total, 120 degrees apart)
for i in range(1, 3):
    angle = i * (360 / 3)
    # Create a copy of the frustum at this angle
    frustum_copy = frustum.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(frustum_copy)

# Create and cut holes: 5mm diameter circles at the center of each frustum
# The holes penetrate through the entire height
for i in range(3):
    angle = i * (360 / 3)
    # Create a hole that goes through the base and frustum
    hole = (
        cq.Workplane("XY")
        .circle(2.5)
        .extrude(-10)
    )
    result = result.cut(hole)

result = result
