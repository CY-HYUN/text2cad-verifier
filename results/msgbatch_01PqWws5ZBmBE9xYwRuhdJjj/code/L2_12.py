import cadquery as cq
import math

# Create the base: stretch a 100mm diameter circle to 10mm thick
base = cq.Workplane("XY").circle(50).extrude(10)

# Create a reference plane 15mm above the top surface of the base
reference_plane_height = 10 + 15

# Create the bottom profile (20mm diameter circle) on the top surface of the base
bottom_profile = cq.Workplane("XY").workplane(offset=10).circle(10)

# Create the top profile (10mm diameter circle) on the reference plane
top_profile = cq.Workplane("XY").workplane(offset=reference_plane_height).circle(5)

# Create the loft (frustum) between the two profiles
loft = cq.Workplane("XY").workplane(offset=10).circle(10).loft([cq.Workplane("XY").workplane(offset=reference_plane_height).circle(5).val()])

# Alternative approach: use the built-in loft functionality
# Create a simple frustum using two circles and loft
frustum = cq.Workplane("XY").circle(10).workplane(offset=15).circle(5).loft()

# Create a circular array of the frustum (3 times, 120 degrees apart)
# We'll create the frustum as a single solid and use array
result = base

# Create the single frustum
single_frustum = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(10)
    .workplane(offset=15)
    .circle(5)
    .loft()
)

# Combine base with the frustum
result = base.union(single_frustum)

# Create circular array of frustums
for i in range(1, 3):
    angle = i * (360 / 3)
    frustum_copy = single_frustum.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(frustum_copy)

# Create holes: 5mm diameter circles at the center of each frustum
# The holes penetrate through the frustum and the base
hole = cq.Workplane("XY").circle(2.5).extrude(-10)  # 5mm diameter = 2.5mm radius

# Create holes for each of the 3 frustums
for i in range(3):
    angle = i * (360 / 3)
    hole_copy = (
        cq.Workplane("XY")
        .circle(2.5)
        .extrude(-10)
    )
    # Rotate the hole position
    result = result.cut(hole_copy)

result = result
