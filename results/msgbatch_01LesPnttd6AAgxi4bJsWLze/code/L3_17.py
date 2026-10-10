import cadquery as cq
import math

# Create the main cylindrical body
radius = 25  # 50mm diameter
length = 100
result = cq.Workplane("XY").cylinder(length, radius, centered=True)

# Create the sine wave groove on the outer surface
# Parameters
groove_depth = 5
groove_width = 8
semicircle_radius = 4
amplitude = 15
theta_steps = 360
reference_position = 50

# Generate the sine groove path
def generate_groove_profile(theta_deg):
    """Generate the Y (axial) position for a given theta (circumferential angle in degrees)"""
    theta_rad = math.radians(theta_deg)
    y = amplitude * math.sin(theta_rad) + reference_position - length/2
    return y

# Create groove by sweeping a semicircular profile along the sine path
# Build the groove path as a 3D curve
groove_points = []
for theta_deg in range(0, 361, 2):
    theta_rad = math.radians(theta_deg)
    y_axial = generate_groove_profile(theta_deg)
    
    # Position on the cylinder surface
    x = radius * math.cos(theta_rad)
    z = radius * math.sin(theta_rad)
    
    groove_points.append((x, y_axial, z))

# Create the groove profile (semicircular cross-section)
# The groove is carved out from the cylinder surface
# We'll use a subtractive approach: create a cylinder with the groove removed

# Build a sequence of semicircular cross-sections positioned along the sine path
groove_edges = []

# Create the groove by defining it as a swept profile
# We need to subtract the groove geometry from the main cylinder

# For each angular position, create a U-shaped groove profile
for i, theta_deg in enumerate(range(0, 360, 5)):
    theta_rad = math.radians(theta_deg)
    y_axial = generate_groove_profile(theta_deg)
    
    # Position on cylinder surface
    x_center = radius * math.cos(theta_rad)
    z_center = radius * math.sin(theta_rad)
    
    # Normal vector pointing outward from cylinder axis
    normal_x = math.cos(theta_rad)
    normal_z = math.sin(theta_rad)
    
    # Create a small cylindrical section with groove carved out
    # The groove is a semicircular indentation
    if i == 0:
        # Create localized groove geometry and subtract it
        for depth_step in range(semicircle_radius + 1):
            local_groove = cq.Workplane("XY").cylinder(
                length=2, 
                radius=radius - (groove_depth - (semicircle_radius - depth_step))
            ).translate((0, 0, 0))

# Simpler approach: create the groove by removing material using a swept shape
# Create multiple thin cylindrical shells at different radii to approximate the sine groove

# Build the final part with grooves by creating a solid with cutouts
# Use a series of translated and rotated semicircular groove profiles

for theta_deg in range(0, 360, 3):
    theta_rad = math.radians(theta_deg)
    y_axial = generate_groove_profile(theta_deg)
    
    # Create a rectangular cutting tool that approximates the groove
    # Position: on the outer surface of the cylinder, following sine path
    groove_cut = (
        cq.Workplane("XZ")
        .sketch()
        .polygon([
            (-groove_width/2, 0),
            (groove_width/2, 0),
            (groove_width/2, groove_depth),
            (-groove_width/2, groove_depth)
        ])
        .finalize()
        .extrude(2)
        .translate((radius - groove_depth/2, y_axial, 0))
        .rotate((0, 1, 0), (0, 0, 0), theta_deg)
    )
    
    result = result.cut(groove_cut)

result = result.translate((0, 0, 0))
