import cadquery as cq
import math

# Create the base cylinder
result = cq.Workplane("XY").cylinder(height=60, radius=15, centered=True)

# Parameters for knurling pattern
radius = 15
height = 60
num_grooves = 6  # Reduced for performance
pitch = 20

# Create V-shaped notch profile for cutting
notch_depth = 2.5
notch_width = 2.4

# Create grooves using a simpler approach with circular patterns
# First set of grooves - helical pattern going one direction
for i in range(num_grooves):
    angle_offset = (360 / num_grooves) * i
    
    # Create a simple V-groove cutter as a rectangular notch rotated helically
    for z_pos in range(-25, 26, 5):
        # Create V-notch at this height
        angle_rad = math.radians(angle_offset + (z_pos / height) * 180)
        
        # Position of the groove on the cylinder surface
        gx = (radius - notch_depth/2) * math.cos(angle_rad)
        gy = (radius - notch_depth/2) * math.sin(angle_rad)
        
        # Create a small rectangular cutting box
        cutter = (
            cq.Workplane("XY")
            .box(notch_width, notch_depth, 3, centered=True)
            .translate((gx, gy, z_pos))
            .rotate((0, 0, 0), (0, 0, 1), angle_offset + (z_pos / height) * 180)
        )
        
        try:
            result = result.cut(cutter)
        except:
            pass

# Second set of grooves - opposite helical pattern
for i in range(num_grooves):
    angle_offset = (360 / num_grooves) * i + (180 / num_grooves)
    
    for z_pos in range(-25, 26, 5):
        # Create V-notch at this height with opposite helix direction
        angle_rad = math.radians(angle_offset - (z_pos / height) * 180)
        
        # Position of the groove on the cylinder surface
        gx = (radius - notch_depth/2) * math.cos(angle_rad)
        gy = (radius - notch_depth/2) * math.sin(angle_rad)
        
        # Create a small rectangular cutting box
        cutter = (
            cq.Workplane("XY")
            .box(notch_width, notch_depth, 3, centered=True)
            .translate((gx, gy, z_pos))
            .rotate((0, 0, 0), (0, 0, 1), angle_offset - (z_pos / height) * 180)
        )
        
        try:
            result = result.cut(cutter)
        except:
            pass

