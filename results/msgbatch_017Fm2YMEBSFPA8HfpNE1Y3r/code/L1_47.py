import cadquery as cq
import math

# Create the main shaft by extruding a circle
shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)

# Create the keyway cut as a separate solid
# Start from XY plane, create a rectangle for the keyway profile
keyway_solid = cq.Workplane("XY").rect(10.0, 80.0, centered=True).extrude(5.0)

# Translate the keyway solid to position it at y=20 (tangent plane)
# and center it along the z-axis at z=40
keyway_solid = keyway_solid.translate((0, 20.0, 40.0))

# Rotate the keyway so it aligns properly (it needs to be oriented in the XZ plane)
# First translate to origin, rotate, then translate back
keyway_solid = keyway_solid.rotate((0, 0, 0), (1, 0, 0), 90)
keyway_solid = keyway_solid.translate((0, 20.0, 0))

# Now perform the cut operation
result = shaft.cut(keyway_solid)
