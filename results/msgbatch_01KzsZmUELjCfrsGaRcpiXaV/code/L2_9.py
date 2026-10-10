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

# Create teeth by building them individually and unioning
tooth_solid = None

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
    
    # Create tooth by drawing polygon and extruding
    tooth_wp = cq.Workplane("XY").moveTo(p1_x, p1_y).lineTo(p2_x, p2_y).lineTo(p3_x, p3_y).close()
    tooth_i = tooth_wp.extrude(thickness)
    
    # Union all teeth
    if tooth_solid is None:
        tooth_solid = tooth_i
    else:
        tooth_solid = tooth_solid.union(tooth_i)

# Combine base ring with teeth
result = base_ring.union(tooth_solid)
