import cadquery as cq
import math

# Create the first hemisphere (left)
# Sphere centered at (-15, 0, 0) with radius 30
sphere1 = cq.Workplane("XY").sphere(30)
sphere1 = sphere1.translate((-15, 0, 0))

# Create the second hemisphere (right)
# Sphere centered at (15, 0, 0) with radius 30
sphere2 = cq.Workplane("XY").sphere(30)
sphere2 = sphere2.translate((15, 0, 0))

# Fuse the two spheres to create a peanut-like shape
result = sphere1.union(sphere2)
