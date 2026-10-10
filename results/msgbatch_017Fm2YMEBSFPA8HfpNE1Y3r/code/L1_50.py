import cadquery as cq
import math

# Create the first cylindrical segment: circle in YZ plane, extruded along +X
# Circle with diameter 20 mm (radius 10 mm) in the YZ plane
first_cylinder = (
    cq.Workplane("YZ")
    .circle(10.0)
    .extrude(50.0)
)

# Create the second cylindrical segment: circle in XZ plane, extruded along +Y
# Position it at the end face of the first cylinder (at x=50)
# Start from the YZ plane at x=50 and extrude along +Y
second_cylinder = (
    cq.Workplane("XZ")
    .transformed(offset=(50.0, 0, 0))
    .circle(10.0)
    .extrude(50.0)
)

# Merge/union the two cylinders to create the 90° elbow fitting
result = first_cylinder.union(second_cylinder)
