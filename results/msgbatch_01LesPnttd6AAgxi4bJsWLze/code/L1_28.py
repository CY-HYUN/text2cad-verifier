import cadquery as cq
import math

# Create a cube with edge length of 60mm
cube = cq.Workplane("XY").box(60, 60, 60)

# Create a sphere with diameter of 61mm (radius of 30.5mm)
sphere = cq.Workplane("XY").sphere(30.5)

# Subtract the sphere from the cube to create the cavity
result = cube.cut(sphere)
