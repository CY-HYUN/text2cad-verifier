import cadquery as cq
import math

# Create a cylinder: circle (diameter 30mm) on XY plane, extruded 60mm along Z
result = cq.Workplane("XY").circle(15.0).extrude(60.0)

# Create a hole by cutting through the cylinder along the Y direction
# Position at the middle height of the cylinder (Z=30)
result = (
    result
    .faces(">Z")
    .workplane(offset=-30.0)
    .circle(5.0)
    .cutThruAll(direction=(0, 1, 0))
)
