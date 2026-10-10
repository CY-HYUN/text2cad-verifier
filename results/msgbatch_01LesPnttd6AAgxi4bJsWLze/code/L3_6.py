import cadquery as cq
import math

# Create the base cylinder
radius = 20  # diameter 40mm
length = 100
result = cq.Workplane("XY").cylinder(length, radius, centered=True)

# Now we need to cut the sine wave groove
# The groove follows a sine wave pattern around the cylinder
# When unrolled: Y = 30*sin(φ), where φ goes from 0 to 360 degrees
# This means axial displacement ranges from -30 to +30 mm as we go around

# Create the groove profile (U-shaped with rounded bottom)
# Width: 6mm, Depth: 4mm, rounded bottom radius: 3mm

# We'll create the groove by sweeping a U-shaped profile along a helical path
# First, create the cross-section profile of the groove
groove_width = 6
groove_depth = 4
corner_radius = 3

# Create a U-shaped profile
# The profile is in the XZ plane, where we cut into the cylinder
profile_points = []

# Left edge
profile_points.append((-groove_width/2, 0))
# Left bottom corner (rounded)
for i in range(45):
    angle = math.radians(i * 2)
    profile_points.append((-groove_width/2 + corner_radius - corner_radius*math.cos(angle), 
                          -corner_radius + corner_radius*math.sin(angle)))
# Bottom
profile_points.append((0, -groove_depth + corner_radius))
# Right bottom corner (rounded)
for i in range(45):
    angle = math.radians(180 - i * 2)
    profile_points.append((groove_width/2 - corner_radius + corner_radius*math.cos(angle), 
                          -groove_depth + corner_radius - corner_radius*math.sin(angle)))
# Right edge
profile_points.append((groove_width/2, 0))

# Create the groove using a sweep along a sine path
# We'll create multiple cross-section cuts along the circumference
num_sections = 360
section_angle = 1  # degree

for section in range(num_sections):
    angle_deg = section * section_angle
    angle_rad = math.radians(angle_deg)
    
    # Calculate axial position based on sine wave
    axial_offset = 30 * math.sin(angle_rad)
    
    # Position on cylinder circumference
    z_pos = axial_offset  # axial position
    x_pos = radius * math.cos(angle_rad)
    y_pos = radius * math.sin(angle_rad)
    
    if section == 0:
        # Create initial cutting solid for the groove
        # Use a small rectangular solid that we'll position and rotate
        cut_width = groove_width + 1
        cut_depth = groove_depth + 1
        cut_tool = cq.Workplane("XY").box(cut_width, 1, cut_depth, centered=True)

# Alternative approach: create groove by subtracting a swept profile
# Create a path that follows the sine wave around the cylinder

# Create cutting tool by sweeping U-profile along sine helical path
def create_groove_profile():
    """Create the U-shaped groove cross-section"""
    # Points for the U-shape in 2D
    points = []
    points.append((0, -groove_depth))
    
    # Rounded bottom
    for i in range(46):
        t = i / 45.0
        angle = t * math.pi
        points.append((corner_radius * math.sin(angle) - groove_width/2, 
                      -groove_depth + corner_radius - corner_radius*math.cos(angle)))
    
    points.append((-groove_width/2, 0))
    points.append((groove_width/2, 0))
    
    # Right rounded section
    for i in range(46):
        t = i / 45.0
        angle = t * math.pi
        points.append((groove_width/2 - corner_radius*math.sin(angle), 
                      -groove_depth + corner_radius - corner_radius*math.cos(angle)))
    
    points.append((0, -groove_depth))
    
    return points

# Create groove using multiple box cuts positioned along sine wave
cut_count = 180
for i in range(cut_count):
    t = i / cut_count
    angle_rad = t * 2 * math.pi
    
    # Sine wave displacement
    z_offset = 30 * math.sin(angle_rad)
    
    # Position on cylinder
    angle_deg = math.degrees(angle_rad)
    
    # Create small cutting box
    box_height = 100 / cut_count + 2
    cut_solid = (cq.Workplane("XY")
                 .box(groove_width + 0.5, box_height, groove_depth + 0.5, centered=True)
                 .translate((0, 0, z_offset)))
    
    # Rotate to cylinder surface
    cut_solid = cut_solid.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    cut_solid = cut_solid.translate((0, 0, 0))
    
    result = result.cut(cut_solid)

