import cadquery as cq
import math

# Create outer hemisphere
outer_sphere = cq.Workplane("XY").sphere(50)

# Create inner hemisphere to subtract
inner_sphere = cq.Workplane("XY").sphere(40)

# Cut the inner sphere from the outer sphere to create a hemispherical shell
# We need to work with half of each sphere (the top half)
# First, create a box to cut away the bottom half of both spheres
cutting_box = cq.Workplane("XY").box(200, 200, 100, centered=True).translate((0, 0, -50))

# Create outer hemisphere by cutting the sphere with a plane at z=0
outer_hemisphere = outer_sphere.cut(cutting_box)

# Create inner hemisphere by cutting the sphere with a plane at z=0
inner_hemisphere = inner_sphere.cut(cutting_box)

# Create the hollow hemispherical shell by subtracting inner from outer
result = outer_hemisphere.cut(inner_hemisphere)
