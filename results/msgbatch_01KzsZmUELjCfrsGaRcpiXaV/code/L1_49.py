import cadquery as cq
import math

# Create a cube with 40mm edge length
cube = cq.Workplane("XY").box(40, 40, 40)

# Create three cylindrical holes along X, Y, and Z axes
# Each hole has a diameter of 10mm (radius 5mm) and extends through the entire cube

# Hole along X-axis (length direction)
hole_x = cq.Workplane("YZ").circle(5).extrude(40, both=True)

# Hole along Y-axis (width direction)
hole_y = cq.Workplane("XZ").circle(5).extrude(40, both=True)

# Hole along Z-axis (thickness direction)
hole_z = cq.Workplane("XY").circle(5).extrude(40, both=True)

# Cut all three holes from the cube
result = cube.cut(hole_x).cut(hole_y).cut(hole_z)

