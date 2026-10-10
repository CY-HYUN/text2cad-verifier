import cadquery as cq
import math

# Create a cube with edge length 50mm
cube = cq.Workplane("XY").box(50, 50, 50)

# Define the diagonal vertices of the cube
# One corner at origin, other at (50, 50, 50)
p1 = (0, 0, 0)
p2 = (50, 50, 50)

# Calculate the center of the cube
center = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2, (p1[2] + p2[2])/2)

# Calculate the diagonal direction vector
diagonal = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
diagonal_length = math.sqrt(diagonal[0]**2 + diagonal[1]**2 + diagonal[2]**2)

# Normalize the diagonal vector
diagonal_normalized = (diagonal[0]/diagonal_length, diagonal[1]/diagonal_length, diagonal[2]/diagonal_length)

# Create a plane perpendicular to the diagonal at the center of the cube
# The normal to the plane is the diagonal direction
# We need to find two perpendicular vectors to create the plane coordinate system

# Find a vector perpendicular to diagonal
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

# Create a workplane at the center with the perpendicular vectors as axes
# Use the center point and perpendicular plane for the circle
plane_origin = cq.Vector(*center)
plane_x_dir = cq.Vector(*cross1_normalized)
plane_y_dir = cq.Vector(*cross2)

# Create a plane perpendicular to diagonal and draw circle on it
wp = cq.Workplane(origin=plane_origin, xDir=plane_x_dir, yDir=plane_y_dir)

# Draw a circle with diameter 10mm (radius 5mm) on this plane
circle = wp.circle(5)

# Extrude the circle along the diagonal direction to cut through the cube
# Use a large distance to ensure complete penetration
extrude_distance = diagonal_length * 2
extrude_dir = cq.Vector(*diagonal_normalized)

# Create the cut profile - extrude the circle perpendicular to its plane
# The extrusion direction should be along the diagonal
result = cube.cut(circle.extrude(extrude_distance, both=True))
