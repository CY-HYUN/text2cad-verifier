import cadquery as cq
import math

# Create the main rectangular prism
prism = cq.Workplane("XY").box(80, 80, 40, centered=True)

# Create a hemisphere to subtract from the top surface
# The hemisphere has radius 20mm and its flat edge should be flush with the top surface
# The top surface of the prism is at z = 20 (half of height 40)
# We need to subtract a hemisphere that goes down from z=20 to z=0 (the center)

# Create a sphere with radius 20mm centered at the origin
sphere = cq.Workplane("XY").sphere(20)

# We only want the top half of the sphere, so we'll cut it with a plane at z=0
# to keep only the hemisphere that extends upward
hemisphere = sphere.cut(cq.Workplane("XY").box(50, 50, 20, centered=True).translate((0, 0, -20)))

# Position the hemisphere so its flat face is flush with the top surface of the prism
# The top surface is at z=20, so we translate the hemisphere up by 20
hemisphere = hemisphere.translate((0, 0, 20))

# Subtract the hemisphere from the prism
result = prism.cut(hemisphere)
