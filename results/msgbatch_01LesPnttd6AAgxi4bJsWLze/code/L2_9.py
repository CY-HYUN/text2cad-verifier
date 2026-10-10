import cadquery as cq
import math

# Base ring parameters
outer_diameter = 80
inner_diameter = 50
thickness = 10
outer_radius = outer_diameter / 2
inner_radius = inner_diameter / 2

# Tooth parameters
num_teeth = 12
tooth_height = 5
tooth_angle = 360 / num_teeth  # angle between teeth
tooth_base_radius = outer_radius

# Create the base ring
base_ring = cq.Workplane("XY").cylinder(thickness, outer_radius, inner_radius)

# Create teeth
teeth = cq.Workplane("XY")

for i in range(num_teeth):
    # Calculate angle for this tooth
    angle_deg = i * tooth_angle
    angle_rad = math.radians(angle_deg)
    
    # Radial tooth direction (pointing outward)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Calculate points for the tooth profile
    # Point 1: Base of tooth on outer radius (radial edge)
    p1_x = tooth_base_radius * cos_a
    p1_y = tooth_base_radius * sin_a
    
    # Point 2: Tip of tooth (straight radial extension)
    p2_x = (tooth_base_radius + tooth_height) * cos_a
    p2_y = (tooth_base_radius + tooth_height) * sin_a
    
    # For the slanted line, calculate the angle of next tooth root
    next_angle_rad = math.radians((i + 0.5) * tooth_angle)
    
    # Point 3: Root of tooth (slanted line endpoint)
    p3_x = tooth_base_radius * math.cos(next_angle_rad)
    p3_y = tooth_base_radius * math.sin(next_angle_rad)
    
    # Create a single tooth as a 3D solid using polyline
    tooth_profile = [
        (p1_x, p1_y, -thickness/2),
        (p2_x, p2_y, -thickness/2),
        (p3_x, p3_y, -thickness/2),
        (p1_x, p1_y, -thickness/2),
    ]
    
    # Create tooth using loft between top and bottom
    bottom_profile = [(p[0], p[1], -thickness/2) for p in tooth_profile]
    top_profile = [(p[0], p[1], thickness/2) for p in tooth_profile]
    
    # Create a face for the tooth at middle height
    tooth_face = cq.Workplane("XY").polyline([
        (p1_x, p1_y),
        (p2_x, p2_y),
        (p3_x, p3_y),
    ]).close()
    
    # Extrude the tooth profile
    if i == 0:
        tooth_solid = cq.Workplane("XY").polyline([
            (p1_x, p1_y),
            (p2_x, p2_y),
            (p3_x, p3_y),
        ]).close().extrude(thickness)
    else:
        tooth_solid_i = cq.Workplane("XY").polyline([
            (p1_x, p1_y),
            (p2_x, p2_y),
            (p3_x, p3_y),
        ]).close().extrude(thickness)
        tooth_solid = tooth_solid.union(tooth_solid_i)

# Combine base ring with teeth
result = base_ring.union(tooth_solid)
