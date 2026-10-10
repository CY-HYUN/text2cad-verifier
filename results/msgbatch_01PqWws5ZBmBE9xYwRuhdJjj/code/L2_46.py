import cadquery as cq
import math

# Create the first hemisphere with flat face towards positive Z-axis
# This is the top hemisphere
hemisphere1 = cq.Workplane("XY").sphere(30).cut(
    cq.Workplane("XY").box(100, 100, 30, centered=True)
)

# Create the second hemisphere with flat face towards negative Z-axis
# This is the bottom hemisphere
hemisphere2 = cq.Workplane("XY").sphere(30).cut(
    cq.Workplane("XY").box(100, 100, 30, centered=True).translate((0, 0, 30))
)

# Actually, let's create this more directly using half-space cuts
# Create a complete sphere
full_sphere = cq.Workplane("XY").sphere(30)

# Cut the sphere in half to get the top hemisphere (flat face at Z=0, dome towards +Z)
hemisphere_top = full_sphere.cut(
    cq.Workplane("XY").box(100, 100, 30, centered=True).translate((0, 0, -30))
)

# Cut the sphere in half to get the bottom hemisphere (flat face at Z=0, dome towards -Z)
hemisphere_bottom = full_sphere.cut(
    cq.Workplane("XY").box(100, 100, 30, centered=True).translate((0, 0, 30))
)

# Perform Boolean union to merge the two hemispheres
result = hemisphere_top.union(hemisphere_bottom)
