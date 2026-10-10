import cadquery as cq
import math

# Create a sphere with radius 25 mm centered at origin
sphere = cq.Solid.makeSphere(25)

# Create a cylinder for the through-hole with diameter 14 mm (radius 7 mm)
# The cylinder needs to be long enough to go completely through the sphere
hole_radius = 7
hole_height = 60  # Longer than the sphere diameter to ensure complete removal

cylinder = cq.Solid.makeCylinder(hole_radius, hole_height, pnt=cq.Vector(0, 0, -30), dir=cq.Vector(0, 0, 1))

# Subtract the cylinder from the sphere to create the through-hole
result = sphere.cut(cylinder)
