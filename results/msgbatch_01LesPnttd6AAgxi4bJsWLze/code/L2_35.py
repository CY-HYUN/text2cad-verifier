import cadquery as cq
import math

# Create the base cube
cube = cq.Workplane("XY").box(60, 60, 60)

# Create a cylinder along X-axis with axis at Z=5mm
# The cylinder needs to go through the entire cube along X
# Center it at Z=5mm, spanning from Y=-30 to Y=30
cylinder_x = cq.Workplane("YZ").circle(10).extrude(60)
# Translate to position the axis at Z=5mm
cylinder_x = cylinder_x.translate((0, 0, 5))

# Create a cylinder along Y-axis with axis at Z=-5mm
# The cylinder needs to go through the entire cube along Y
# Center it at Z=-5mm, spanning from X=-30 to X=30
cylinder_y = cq.Workplane("XZ").circle(10).extrude(60)
# Translate to position the axis at Z=-5mm
cylinder_y = cylinder_y.translate((0, 0, -5))

# Subtract both cylinders from the cube to create the through-holes
result = cube.cut(cylinder_x).cut(cylinder_y)
