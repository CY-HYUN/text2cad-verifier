import cadquery as cq
import math

# Create the main circular disk
disk = cq.Workplane("XY").circle(50).extrude(12)

# Define the hole positions (at radius 35mm, at 0°, 90°, 180°, 270°)
hole_positions = [
    (35, 0),
    (0, 35),
    (-35, 0),
    (0, -35)
]

# Create the part by drilling holes
result = disk

for x, y in hole_positions:
    # Drill a through hole at each position
    result = result.faces(">Z").workplane().center(x, y).circle(5).cutThruAll()

# Apply chamfer to the top edges of the holes
# Get all edges on the top face and filter for circular edges (the hole edges)
result = result.faces(">Z").edges().chamfer(0.8)

