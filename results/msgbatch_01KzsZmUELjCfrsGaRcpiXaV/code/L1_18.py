import cadquery as cq
import math

# Create the capsule shape
# Cylinder in the middle: diameter 30mm (radius 15mm), length 60mm
# Hemispheres at both ends: radius 15mm

radius = 15
cylinder_length = 60

# Create the cylinder centered at origin, along Z-axis
cylinder = cq.Workplane("XY").circle(radius).extrude(cylinder_length)

# Create hemisphere at the top by creating a sphere and cutting it in half
sphere_top = cq.Workplane("XY").sphere(radius).translate((0, 0, cylinder_length / 2))
# Cut away the bottom half of the sphere using a box
box_cut_top = cq.Workplane("XY").box(50, 50, radius, centered=True).translate((0, 0, cylinder_length / 2 - radius))
hemisphere_top = sphere_top.cut(box_cut_top)

# Create hemisphere at the bottom by creating a sphere and cutting it in half
sphere_bottom = cq.Workplane("XY").sphere(radius).translate((0, 0, -cylinder_length / 2))
# Cut away the top half of the sphere using a box
box_cut_bottom = cq.Workplane("XY").box(50, 50, radius, centered=True).translate((0, 0, -cylinder_length / 2 + radius))
hemisphere_bottom = sphere_bottom.cut(box_cut_bottom)

# Combine all parts
result = cylinder.union(hemisphere_top).union(hemisphere_bottom)
