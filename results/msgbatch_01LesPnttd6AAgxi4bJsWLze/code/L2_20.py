import cadquery as cq
import math

# Create base cube
cube = cq.Workplane("XY").box(50, 50, 50)

# Body diagonal of a cube goes from one vertex to the opposite vertex
# For a cube centered at origin with edge length 50, vertices are at (±25, ±25, ±25)
# Body diagonal direction: from (-25, -25, -25) to (25, 25, 25)
# Direction vector: (1, 1, 1) normalized

# Calculate the body diagonal direction and length
diagonal_start = (-25, -25, -25)
diagonal_end = (25, 25, 25)
diagonal_vector = (
    diagonal_end[0] - diagonal_start[0],
    diagonal_end[1] - diagonal_start[1],
    diagonal_end[2] - diagonal_start[2]
)
diagonal_length = math.sqrt(sum(x**2 for x in diagonal_vector))
diagonal_normalized = tuple(x / diagonal_length for x in diagonal_vector)

# Calculate rotation angles to align Z-axis with body diagonal
# Body diagonal direction is (1, 1, 1) normalized
# We need to rotate so this direction aligns with (0, 0, 1)

# First, project diagonal onto XY plane to get the azimuth angle
azimuth = math.atan2(diagonal_normalized[1], diagonal_normalized[0])

# Calculate the polar angle (angle from Z-axis)
polar = math.acos(diagonal_normalized[2])

# Convert to degrees
azimuth_deg = math.degrees(azimuth)
polar_deg = math.degrees(polar)

# Create a cylinder along Z-axis with diameter 10mm and sufficient length
hole_cylinder = cq.Workplane("XY").cylinder(diagonal_length + 10, 5, centered=True)

# Rotate the cylinder to align with body diagonal
# First rotate around Z by azimuth angle, then rotate around Y by polar angle
hole_cylinder = hole_cylinder.rotate((0, 0, 0), (0, 0, 1), azimuth_deg)
hole_cylinder = hole_cylinder.rotate((0, 0, 0), (0, 1, 0), polar_deg)

# Cut the hole from the cube
result = cube.cut(hole_cylinder)
