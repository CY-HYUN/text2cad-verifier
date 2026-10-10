import cadquery as cq
import math

# Create the main disc
outer_diameter = 100
thickness = 20
inner_hole_diameter = 60

# Start with a solid cylinder (the main disc)
result = cq.Workplane("XY").cylinder(thickness, outer_diameter / 2)

# Cut out the central hole
result = result.cut(cq.Workplane("XY").cylinder(thickness, inner_hole_diameter / 2))

# Add the teeth on the inner circumference
num_teeth = 12
tooth_width = 5
tooth_height = 5
inner_radius = inner_hole_diameter / 2

# Calculate the angle between each tooth
angle_step = 360 / num_teeth

# Create teeth
for i in range(num_teeth):
    # Calculate the angle for this tooth
    angle = i * angle_step
    
    # Convert angle to radians
    angle_rad = math.radians(angle)
    
    # Calculate the position of the tooth center (radially outward from inner hole)
    tooth_center_radius = inner_radius + tooth_height / 2
    tooth_x = tooth_center_radius * math.cos(angle_rad)
    tooth_y = tooth_center_radius * math.sin(angle_rad)
    
    # Create a rectangular tooth box
    # The tooth extends from the inner hole wall towards the center
    tooth_box = (
        cq.Workplane("XY")
        .box(tooth_width, tooth_height, thickness, centered=True)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((inner_radius + tooth_height / 2, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    
    # Use a simpler approach: create tooth as a box and position it
    tooth = cq.Workplane("XY").box(tooth_width, tooth_height, thickness, centered=True)
    
    # Translate tooth to correct position
    tooth = tooth.translate((inner_radius + tooth_height / 2, 0, 0))
    
    # Rotate tooth to correct angular position
    tooth = tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    
    # Union the tooth to the result
    result = result.union(tooth)

