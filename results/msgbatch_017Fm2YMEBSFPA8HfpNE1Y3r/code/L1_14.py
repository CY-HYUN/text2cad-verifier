import cadquery as cq
import math

# Create a cylinder: circle on XY plane extruded 20mm
cylinder = cq.Workplane("XY").circle(25.0).extrude(20.0)

# Create a cone: draw a right triangle on XZ plane and revolve around Z-axis
# The triangle has a base of 25mm (radius) and height of 40mm
cone = (
    cq.Workplane("XZ")
    .polyline([(0, 20.0), (25.0, 20.0), (0, 60.0), (0, 20.0)])
    .close()
    .revolve()
)

# Merge the cylinder and cone to create the final body
result = cylinder.union(cone)
