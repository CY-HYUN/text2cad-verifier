import cadquery as cq
import math

# Create the capsule shape
# Cylinder in the middle: diameter 30mm (radius 15mm), length 60mm
# Hemispheres at both ends: radius 15mm

radius = 15
cylinder_length = 60

# Create the cylinder (centered at origin, along Z-axis)
cylinder = cq.Workplane("XY").circle(radius).extrude(cylinder_length)

# Create a hemisphere for the top end
# A hemisphere with radius 15mm at the top (z = cylinder_length/2)
hemisphere_top = (
    cq.Workplane("XY")
    .sphere(radius)
    .translate((0, 0, cylinder_length / 2))
)

# Create a hemisphere for the bottom end
# A hemisphere with radius 15mm at the bottom (z = -cylinder_length/2)
hemisphere_bottom = (
    cq.Workplane("XY")
    .sphere(radius)
    .translate((0, 0, -cylinder_length / 2))
)

# We need to cut the spheres in half to create hemispheres
# Create cutting planes
cutting_plane_top = cq.Workplane("XY").plane(cylinder_length / 2).cutThruAll()
cutting_plane_bottom = cq.Workplane("XY").plane(-cylinder_length / 2).cutThruAll()

# Create a full sphere at top and cut it
sphere_top = cq.Workplane("XY").sphere(radius).translate((0, 0, cylinder_length / 2))
# Create a box to cut away the bottom half
box_top = cq.Workplane("XY").box(100, 100, radius, centered=True).translate((0, 0, cylinder_length / 2 + radius / 2))
hemisphere_top = sphere_top.cut(box_top)

# Create a full sphere at bottom and cut it
sphere_bottom = cq.Workplane("XY").sphere(radius).translate((0, 0, -cylinder_length / 2))
# Create a box to cut away the top half
box_bottom = cq.Workplane("XY").box(100, 100, radius, centered=True).translate((0, 0, -cylinder_length / 2 - radius / 2))
hemisphere_bottom = sphere_bottom.cut(box_bottom)

# Combine all parts
result = cylinder.union(hemisphere_top).union(hemisphere_bottom)
