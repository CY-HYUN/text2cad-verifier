import cadquery as cq
import math

# Create the base ring
outer_diameter = 100
inner_diameter = 60
thickness = 20

# Create the main ring
ring = cq.Workplane("XY").cylinder(thickness, outer_diameter/2, inner_diameter/2)

# Tooth dimensions
tooth_width = 5
tooth_depth = 3
tooth_height = 20
inner_radius = inner_diameter / 2

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
