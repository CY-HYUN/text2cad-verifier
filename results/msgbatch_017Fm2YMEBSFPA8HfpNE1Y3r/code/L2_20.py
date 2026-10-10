import cadquery as cq
import math

# Create a cube with edge length 50mm
cube = cq.Workplane("XY").box(50, 50, 50)

# Define the diagonal vertices of the cube
p1 = (0, 0, 0)
p2 = (50, 50, 50)

# Calculate the center of the cube
center = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2, (p1[2] + p2[2])/2)

# Calculate the diagonal direction vector
diagonal = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
diagonal_length = math.sqrt(diagonal[0]**2 + diagonal[1]**2 + diagonal[2]**2)

# Normalize the diagonal vector
diagonal_normalized = (diagonal[0]/diagonal_length, diagonal[1]/diagonal_length, diagonal[2]/diagonal_length)

# Find two perpendicular vectors to the diagonal
if abs(diagonal_normalized[0]) < 0.9:
    perp1 = (1, 0, 0)
else:
    perp1 = (0, 1, 0)

# Cross product to get first perpendicular vector
cross1 = (
    diagonal_normalized[1] * perp1[2] - diagonal_normalized[2] * perp1[1],
    diagonal_normalized[2] * perp1[0] - diagonal_normalized[0] * perp1[2],
    diagonal_normalized[0] * perp1[1] - diagonal_normalized[1] * perp1[0]
)
cross1_length = math.sqrt(cross1[0]**2 + cross1[1]**2 + cross1[2]**2)
cross1_normalized = (cross1[0]/cross1_length, cross1[1]/cross1_length, cross1[2]/cross1_length)

# Second perpendicular vector via cross product
cross2 = (
    diagonal_normalized[1] * cross1_normalized[2] - diagonal_normalized[2] * cross1_normalized[1],
    diagonal_normalized[2] * cross1_normalized[0] - diagonal_normalized[0] * cross1_normalized[2],
    diagonal_normalized[0] * cross1_normalized[1] - diagonal_normalized[1] * cross1_normalized[0]
)

# Create workplane at center
wp = cq.Workplane("XY").transformed(offset=cq.Vector(*center))

# Draw circle with diameter 10mm (radius 5mm)
circle = wp.circle(5)

# Create the cutting tool by extruding the circle along the diagonal direction
# Use a large distance to ensure complete penetration
extrude_distance = diagonal_length * 2

# Create extrusion direction vector
extrude_dir = cq.Vector(*diagonal_normalized)

# Extrude in both directions along the diagonal to cut through
cutting_tool = circle.extrude(extrude_distance, both=True)

# Transform the cutting tool so it aligns with the diagonal
# Rotate it to align with diagonal direction
# Start from default Z-axis orientation and rotate to diagonal
cutting_tool = cutting_tool.rotate((0, 0, 0), cross1_normalized, 90).rotate((0, 0, 0), cross2, 45)

# Perform the cut
result = cube.cut(circle.extrude(extrude_distance, both=True))
