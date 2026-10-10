import cadquery as cq
import math

# Create the base cube
base_cube = cq.Solid.makeBox(60, 60, 60, pnt=cq.Vector(-30, -30, -30))

# Create cylinders for the holes to cut through all six faces
# We'll cut circular holes with diameter 40mm (radius 20mm) through the center along each axis

# Hole along X axis (through left and right faces)
hole_x = cq.Solid.makeCylinder(20, 120, pnt=cq.Vector(-60, 0, 0), dir=cq.Vector(1, 0, 0))

# Hole along Y axis (through front and back faces)
hole_y = cq.Solid.makeCylinder(20, 120, pnt=cq.Vector(0, -60, 0), dir=cq.Vector(0, 1, 0))

# Hole along Z axis (through top and bottom faces)
hole_z = cq.Solid.makeCylinder(20, 120, pnt=cq.Vector(0, 0, -60), dir=cq.Vector(0, 0, 1))

# Cut all three holes from the base cube to create the frame
frame = base_cube.cut(hole_x).cut(hole_y).cut(hole_z)

# Create the sphere with diameter 30mm (radius 15mm) at the center
sphere = cq.Solid.makeSphere(15, pnt=cq.Vector(0, 0, 0))

# Combine the frame and sphere
result = frame.union(sphere)
