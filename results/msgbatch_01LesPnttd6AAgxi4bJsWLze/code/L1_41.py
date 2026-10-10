import cadquery as cq
import math

# Create the main disc
disc = cq.Workplane("XY").cylinder(height=10, radius=50)

# Define the positions of the four holes on a circle of radius 35mm
hole_radius = 35
hole_diameter = 10
hole_positions = [
    (0, hole_radius),      # Top
    (hole_radius, 0),      # Right
    (0, -hole_radius),     # Bottom
    (-hole_radius, 0)      # Left
]

# Create holes at each position
for x, y in hole_positions:
    disc = disc.faces(">Z").workplane().moveTo(x, y).hole(hole_diameter)

result = disc
