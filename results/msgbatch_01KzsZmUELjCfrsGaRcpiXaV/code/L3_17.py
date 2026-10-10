import cadquery as cq
import math

# Create the main cylindrical body
radius = 25  # 50mm diameter
length = 100
result = cq.Workplane("XY").cylinder(length, radius)

# Parameters for the sine groove
groove_depth = 5
groove_width = 8
semicircle_radius = 4
amplitude = 15
reference_position = 50

# Generate the sine wave axial position for a given circumferential angle
def generate_groove_axial_position(theta_deg):
    """Generate the axial (Y) position for a given theta (circumferential angle in degrees)"""
    theta_rad = math.radians(theta_deg)
    y = amplitude * math.sin(theta_rad) + reference_position - length/2
    return y

# Create the groove by subtracting material from the cylinder
# We'll create small groove segments at regular angular intervals
for theta_deg in range(0, 360, 4):
    theta_rad = math.radians(theta_deg)
    y_axial = generate_groove_axial_position(theta_deg)
    
    # Create a groove cutting tool - a rectangular block positioned on the cylinder surface
    # The block is oriented radially outward
    groove_cut = (
        cq.Workplane("XY")
        .box(groove_width, 2, groove_depth)
        .translate((radius - groove_depth/2, 0, 0))
        .rotate((0, 0, 1), (0, 0, 0), theta_deg)
        .translate((0, y_axial, 0))
    )
    
    result = result.cut(groove_cut)

# Create a more refined groove with semicircular bottom by additional material removal
# Add semicircular indents to create the U-shaped profile
for theta_deg in range(0, 360, 6):
    theta_rad = math.radians(theta_deg)
    y_axial = generate_groove_axial_position(theta_deg)
    
    # Create a semicircular cutting profile
    semi_cut = (
        cq.Workplane("XZ")
        .circle(semicircle_radius)
        .extrude(groove_width)
        .translate((radius - groove_depth, y_axial, 0))
        .rotate((0, 0, 1), (0, 0, 0), theta_deg)
    )
    
    result = result.cut(semi_cut)
