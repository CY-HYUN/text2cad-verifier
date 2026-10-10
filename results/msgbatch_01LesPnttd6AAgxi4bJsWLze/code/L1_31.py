import cadquery as cq
import math

# Create a sphere with radius 25mm
sphere = cq.Workplane("XY").sphere(25)

# Create a square prism (cube-like) that will be used to cut through the sphere
# The square has side length 20mm and needs to be tall enough to go through the entire sphere
# Height should be at least 2*radius = 50mm to ensure it cuts all the way through
square_hole = cq.Workplane("XY").box(20, 20, 60, centered=True)

# Cut the square hole from the sphere
result = sphere.cut(square_hole)
