import cadquery as cq
import math

# Create a cylinder: circle (diameter 30mm) on XY plane, extruded 60mm along Z
base_cylinder = cq.Workplane("XY").circle(15.0).extrude(60.0)

# Create a sketch on the XZ plane with a circle (diameter 10mm) at point (0, 30.0)
# The point (0, 30.0) in XZ plane means X=0, Z=30.0
# We need to create a hole that goes through the cylinder along the Y direction
# Position the sketch at Z=30 (middle height of the cylinder)
hole_sketch = (
    cq.Workplane("XZ")
    .moveTo(0, 30.0)  # Move to (0, 30.0) in the XZ plane
    .circle(5.0)  # Circle with diameter 10mm (radius 5mm)
)

# Perform an extruded cut through the entire part along the Y direction
# We cut from Y=-20 to Y=20 to ensure we go through the entire cylinder
result = base_cylinder.cutBlind(
    hole_sketch.extrude(40.0, taper=0).val(),
    depth=40.0
)

# Alternative approach using a more direct method:
result = cq.Workplane("XY").circle(15.0).extrude(60.0)
result = result.faces(">Z").workplane().transformed(offset=(0, 0, -30)).circle(5.0).cutThruAll(direction=(0, 1, 0))

# Simpler and more direct approach:
result = (
    cq.Workplane("XY")
    .circle(15.0)
    .extrude(60.0)
    .faces(">Z")
    .workplane(offset=-30.0)
    .circle(5.0)
    .cutThruAll(direction=(0, 1, 0))
)
