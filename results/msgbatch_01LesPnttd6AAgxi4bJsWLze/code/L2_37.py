import cadquery as cq
import math

# Create the central sphere
sphere = cq.Solid.makeSphere(20)

# Create a cylinder and position it
def create_cylinder(length, radius, position_axis, direction):
    """
    Create a cylinder along a specified axis.
    position_axis: 'X', 'Y', or 'Z'
    direction: 1 for positive, -1 for negative
    """
    # Create cylinder along Z axis initially (default CadQuery orientation)
    cylinder = cq.Solid.makeCylinder(radius, length)
    
    # Translate cylinder so one end is at origin and extends outward
    # The cylinder is created centered, so we need to move it
    half_length = length / 2
    
    # Move cylinder to extend from the sphere surface
    if position_axis == 'X':
        # Rotate to align with X axis and position
        cylinder = cylinder.rotate((0, 0, 0), (0, 1, 0), 90)
        offset = 20 + length / 2  # Sphere radius + half cylinder length
        cylinder = cylinder.translate((direction * offset, 0, 0))
    elif position_axis == 'Y':
        # Rotate to align with Y axis and position
        cylinder = cylinder.rotate((0, 0, 0), (1, 0, 0), -90)
        offset = 20 + length / 2
        cylinder = cylinder.translate((0, direction * offset, 0))
    elif position_axis == 'Z':
        # Already aligned with Z axis
        offset = 20 + length / 2
        cylinder = cylinder.translate((0, 0, direction * offset))
    
    return cylinder

# Create blind holes in each cylinder
def create_blind_hole(cylinder_length, hole_radius, hole_depth, position_axis, direction):
    """
    Create a cylinder representing the blind hole at the end of each cantilever.
    """
    hole = cq.Solid.makeCylinder(hole_radius, hole_depth)
    
    # Position at the end of the cylinder
    hole_center_distance = 20 + cylinder_length  # From origin to hole center
    
    if position_axis == 'X':
        hole = hole.rotate((0, 0, 0), (0, 1, 0), 90)
        hole_pos = direction * (hole_center_distance - hole_depth / 2)
        hole = hole.translate((hole_pos, 0, 0))
    elif position_axis == 'Y':
        hole = hole.rotate((0, 0, 0), (1, 0, 0), -90)
        hole_pos = direction * (hole_center_distance - hole_depth / 2)
        hole = hole.translate((0, hole_pos, 0))
    elif position_axis == 'Z':
        hole_pos = direction * (hole_center_distance - hole_depth / 2)
        hole = hole.translate((0, 0, hole_pos))
    
    return hole

# Build the structure
result = sphere

# Cylinder parameters
cyl_radius = 15 / 2  # radius = diameter / 2
cyl_length = 30
hole_radius = 8 / 2
hole_depth = 10

# Create six cylinders (positive and negative X, Y, Z)
for axis in ['X', 'Y', 'Z']:
    for direction in [1, -1]:
        cyl = create_cylinder(cyl_length, cyl_radius, axis, direction)
        result = result.union(cyl)

# Create and subtract blind holes from each cylinder
holes_to_subtract = cq.Solid.makeSphere(0.1)  # Start with a tiny sphere as placeholder

for axis in ['X', 'Y', 'Z']:
    for direction in [1, -1]:
        hole = create_blind_hole(cyl_length, hole_radius, hole_depth, axis, direction)
        holes_to_subtract = holes_to_subtract.union(hole)

# Subtract all holes from the result
result = result.cut(holes_to_subtract)
