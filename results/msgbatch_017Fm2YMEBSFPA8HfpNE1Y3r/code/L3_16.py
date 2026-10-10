import cadquery as cq
import math

# Create a series of cross-sectional profiles at different X positions
# These will be lofted together to form the mouse body

def create_profile_at_x(x_pos):
    """Create a cross-sectional profile at a given X position"""
    
    # Calculate spine height using quadratic interpolation
    if x_pos <= 55:
        t = x_pos / 55.0
        spine_height = 35 * (2 * t * (1 - t) + t * t)
    else:
        t = (x_pos - 55) / 55.0
        spine_height = 35 * (1 - t) * (1 - t)
    
    # Width varies along the length
    width_factor = 0.5 + 0.5 * math.cos(math.pi * x_pos / 110.0)
    bottom_y_max = 20 * width_factor
    
    # Create an arched profile: points from bottom-left to bottom-right
    profile_points = [
        cq.Vector(x_pos, -bottom_y_max, 0),
        cq.Vector(x_pos, -bottom_y_max * 0.6, spine_height * 0.25),
        cq.Vector(x_pos, -bottom_y_max * 0.2, spine_height * 0.6),
        cq.Vector(x_pos, 0, spine_height),
        cq.Vector(x_pos, bottom_y_max * 0.2, spine_height * 0.6),
        cq.Vector(x_pos, bottom_y_max * 0.6, spine_height * 0.25),
        cq.Vector(x_pos, bottom_y_max, 0)
    ]
    
    return profile_points

# Define X-positions for cross-sections
x_positions = [0, 35, 70, 110]

# Create profile wires for lofting
wires = []

for x_pos in x_positions:
    profile_points = create_profile_at_x(x_pos)
    
    # Create a wire from the profile points
    wire = cq.Workplane("XY").polyline(profile_points).close().val()
    wires.append(wire)

# Create the lofted solid by lofting between consecutive profiles
result = cq.Workplane("XY").loft(wires, ruled=False)

# Thicken the surface inward by 2.0mm to create a solid shell
result = result.shell(2.0)

# Ensure result is a valid solid
result = result.val()
