import cadquery as cq
import math

# Create the base ring
outer_diameter = 100
inner_diameter = 60
thickness = 20

# Create the main ring
ring = cq.Workplane("XY").cylinder(thickness, outer_diameter/2, inner_diameter/2)

# Now create the tooth feature
# Tooth dimensions
tooth_width = 5
tooth_depth = 3
tooth_height = 20
inner_radius = inner_diameter / 2

# Create a single tooth on the inner face
# The tooth extends from the inner edge towards center
tooth = (cq.Workplane("XY")
         .rect(tooth_width, tooth_depth)
         .extrude(tooth_height))

# Position the tooth at the inner edge
# Position it so it extends radially inward from the inner hole
tooth_y_pos = inner_radius - tooth_depth / 2  # Center of tooth in Y direction
tooth = tooth.translate((0, tooth_y_pos, 0))

# Create a pattern with the tooth
# We need to use circular array to replicate the tooth 12 times
# First, create a combined shape with one tooth
tooth_extrusion = (cq.Workplane("XY")
                   .rect(tooth_width, tooth_depth)
                   .extrude(tooth_height))

# Position tooth at correct radial distance
tooth_extrusion = tooth_extrusion.translate((0, inner_radius - tooth_depth / 2, 0))

# Start with the ring
result = ring

# Create the tooth pattern by rotating and adding teeth
num_teeth = 12
angle_step = 360 / num_teeth

for i in range(num_teeth):
    angle = i * angle_step
    # Create tooth for this position
    tooth_feature = (cq.Workplane("XY")
                     .rect(tooth_width, tooth_depth)
                     .extrude(tooth_height))
    # Position at inner edge, radially outward
    tooth_feature = tooth_feature.translate((0, inner_radius - tooth_depth / 2, 0))
    # Rotate around Z axis
    tooth_feature = tooth_feature.rotate((0, 0, 0), (0, 0, 1), angle)
    # Union with the ring
    result = result.union(tooth_feature)

