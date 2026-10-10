import cadquery as cq
import math

# Create outer sphere with radius 50mm
outer_sphere = cq.Workplane("XY").sphere(50.0)

# Create inner sphere with radius 40mm
inner_sphere = cq.Workplane("XY").sphere(40.0)

# Split outer sphere by XY plane and keep upper hemisphere (z >= 0)
# We do this by cutting with a box that extends below the XY plane
outer_hemisphere = outer_sphere.cut(
    cq.Workplane("XY").box(200, 200, 100, centered=True).translate((0, 0, -50))
)

# Split inner sphere by XY plane and keep upper hemisphere (z >= 0)
inner_hemisphere = inner_sphere.cut(
    cq.Workplane("XY").box(200, 200, 100, centered=True).translate((0, 0, -50))
)

# Perform difference operation: subtract inner hemisphere from outer hemisphere
result = outer_hemisphere.cut(inner_hemisphere)
