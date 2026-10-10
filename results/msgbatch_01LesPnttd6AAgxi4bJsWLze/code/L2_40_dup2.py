import cadquery as cq
import math

# Create the base cylinder
diameter = 30
radius = diameter / 2
length = 60

# Start with a basic cylinder
base_cylinder = cq.Workplane("XY").cylinder(length, radius)

# Parameters for the helical grooves
groove_depth = 1
spacing = 2
helix_angle = 45  # degrees

# Create a pattern of V-grooves using a series of cutting operations
# We'll approximate the helical pattern using multiple rotated groove patterns

# Convert angle to radians
angle_rad = math.radians(helix_angle)

# Number of complete rotations along the cylinder
num_rotations = length / (spacing * 2)

# Create grooves by making a series of cuts
# We'll use a helical pattern approximation with rectangular cutting boxes

# For the right-handed helix
result = base_cylinder

# Create a cutting tool that represents the V-groove pattern
# We'll create grooves by extruding a V-shaped profile along a helical path
# approximated by multiple straight cuts at angles

# Create the first set of right-handed helical grooves
for i in range(int(length / spacing) + 2):
    z_position = i * spacing - length/2
    
    # Create a cutting plane at an angle
    # Right-handed helix at 45 degrees
    cut_box = (cq.Workplane("XY")
               .box(diameter + 10, groove_depth * 2, spacing + 1)
               .translate((0, radius - groove_depth/2, z_position)))
    
    result = result.cut(cut_box)

# Create the second set of left-handed helical grooves
for i in range(int(length / spacing) + 2):
    z_position = i * spacing - length/2
    
    # Left-handed helix at 45 degrees (opposite direction)
    cut_box = (cq.Workplane("XY")
               .box(diameter + 10, groove_depth * 2, spacing + 1)
               .translate((0, radius - groove_depth/2, z_position))
               .rotateAboutCenter((0, 0, 1), 90))
    
    result = result.cut(cut_box)

# Refine by creating a more accurate knurled pattern
# using a series of V-groove cuts approximated by angled cuts

result = cq.Workplane("XY").cylinder(length, radius)

# Create helical groove pattern more accurately
for rotation in range(int(360 / 10)):
    angle = rotation * 10
    
    for axial_pos in range(int(length / spacing)):
        z_pos = axial_pos * spacing - length/2
        
        # Right-handed grooves
        groove1 = (cq.Workplane("XY")
                   .box(2, groove_depth * 3, spacing + 0.5)
                   .translate((radius - groove_depth/2, 0, z_pos))
                   .rotateAboutCenter((0, 0, 1), angle))
        result = result.cut(groove1)
        
        # Left-handed grooves (perpendicular)
        groove2 = (cq.Workplane("XY")
                   .box(2, groove_depth * 3, spacing + 0.5)
                   .translate((radius - groove_depth/2, 0, z_pos))
                   .rotateAboutCenter((0, 0, 1), angle + 90))
        result = result.cut(groove2)

result = result.cylinder(length, radius)
