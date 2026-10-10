import cadquery as cq
import math

# Create a hemisphere with radius 40mm
# Start with a sphere and cut it in half
sphere = cq.Workplane("XY").sphere(40)
hemisphere = sphere.cut(cq.Workplane("XY").box(100, 100, 50, centered=True).translate((0, 0, -50)))

# Create the cross-shaped groove by cutting
# The groove consists of two rectangular cuts that form a cross pattern
# Each arm of the cross is 16mm wide and extends across the hemisphere

# Create the first arm of the cross (along X-axis)
# Make it deep enough to cut significantly into the hemisphere
arm1 = cq.Workplane("XY").box(80, 16, 30, centered=True)

# Create the second arm of the cross (along Y-axis)
arm2 = cq.Workplane("XY").box(16, 80, 30, centered=True)

# Combine the two arms to create the cross-shaped cutting tool
cross_cutter = arm1.union(arm2)

# Cut the cross groove from the hemisphere
result = hemisphere.cut(cross_cutter)
