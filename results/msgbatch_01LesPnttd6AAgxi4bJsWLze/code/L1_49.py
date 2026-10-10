import cadquery as cq
import math

# Create a cube with 40mm edge length
cube = cq.Solid.makeCube(40, 40, 40)

# Create three cylindrical holes along X, Y, and Z axes
# Each hole has a diameter of 10mm (radius 5mm) and extends through the entire cube

# Hole along X-axis (length direction)
hole_x = cq.Solid.makeCylinder(5, 40, pnt=cq.Vector(-20, 0, 0), dir=cq.Vector(1, 0, 0))

# Hole along Y-axis (width direction)
hole_y = cq.Solid.makeCylinder(5, 40, pnt=cq.Vector(0, -20, 0), dir=cq.Vector(0, 1, 0))

# Hole along Z-axis (thickness direction)
hole_z = cq.Solid.makeCylinder(5, 40, pnt=cq.Vector(0, 0, -20), dir=cq.Vector(0, 0, 1))

# Cut all three holes from the cube
result = cube.cut(hole_x).cut(hole_y).cut(hole_z)
