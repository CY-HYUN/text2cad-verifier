import cadquery as cq
import math

# Create the main shaft by extruding a circle
shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)

# Create a keyway by cutting a rectangle from the shaft
# The keyway is on a plane at y=+20.0 mm
# We need to position a sketch on that plane and cut it into the shaft

# Create a workplane at z=0, y=20 (the tangent plane)
keyway_plane = cq.Workplane("XZ").transformed(offset=(0, 20.0, 0))

# Draw the keyway profile: rectangle 80mm (Z-axis) x 10mm (X-axis), centered at z=40mm
# The rectangle spans from x=-5 to x=+5 (width 10mm) and z=0 to z=80 (length 80mm)
keyway_sketch = keyway_plane.rect(10.0, 80.0, centered=True)

# Extrude (cut) the keyway in the -Y direction with depth 5.0 mm
keyway_cut = keyway_sketch.extrude(-5.0, combine='cut')

# Apply the cut to the shaft
result = shaft.cut(keyway_cut)
