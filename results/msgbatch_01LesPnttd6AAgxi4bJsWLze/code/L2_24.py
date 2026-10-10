import cadquery as cq
import math

# Create the main cylinder body
cylinder = cq.Workplane("XY").cylinder(height=60, radius=20, centered=True)

# Create a sphere for the internal cavity
sphere = cq.Workplane("XY").sphere(radius=15)

# Create the through-hole on top
hole = cq.Workplane("XY").cylinder(height=70, radius=5, centered=True)

# Combine: Start with cylinder, subtract the spherical cavity and the through-hole
result = cylinder.cut(sphere).cut(hole)
