import cadquery as cq
import math

# Initialize and create base manifold block
base = cq.Workplane("XY").rect(200.0, 100.0).extrude(80.0)

# Create internal longitudinal main oil passage (for reference during drilling)
# This is a 20mm diameter cylinder running along the length at center height
internal_passage = cq.Workplane("XY").center(0, 0).circle(10.0).extrude(200.0)

# Drill three horizontal blind holes on front (XZ plane) at center height
# These are oil inlets at equal intervals
drilling_block = base
# Switch to front face (XZ plane)
drilling_block = drilling_block.faces("+Y").workplane().center(0, 0)
# Create three holes at x positions: -60, 0, 60 mm
for x_pos in [-60.0, 0.0, 60.0]:
    drilling_block = drilling_block.moveTo(x_pos, 0).hole(20.0, 60.0)

# Create top surface distribution holes (two rows of five circles each)
top_holes = drilling_block.faces("+Z").workplane()
# Row 1: 5 holes
for i in range(5):
    x_pos = -80.0 + i * 40.0
    y_pos = -20.0
    top_holes = top_holes.moveTo(x_pos, y_pos).hole(10.0, 50.0)

# Row 2: 5 holes
for i in range(5):
    x_pos = -80.0 + i * 40.0
    y_pos = 20.0
    top_holes = top_holes.moveTo(x_pos, y_pos).hole(10.0, 50.0)

# Add countersunk bolt holes at four corners of top surface
corner_holes = top_holes
corners = [(-100.0, -50.0), (100.0, -50.0), (-100.0, 50.0), (100.0, 50.0)]
for corner_x, corner_y in corners:
    # Countersunk hole: outer diameter 12mm, inner hole 8mm, depth 8mm
    corner_holes = corner_holes.moveTo(corner_x, corner_y).hole(8.0, 80.0)
    # Add countersink
    corner_holes = corner_holes.faces("+Z").workplane().moveTo(corner_x, corner_y).hole(12.0, 8.0)

# Create oval grooves on bottom and side surfaces for weight reduction
result = corner_holes

# Add four oval weight reduction grooves on bottom
bottom_workplane = result.faces("-Z").workplane()
oval_positions = [(-60.0, -25.0), (60.0, -25.0), (-60.0, 25.0), (60.0, 25.0)]

for oval_x, oval_y in oval_positions:
    # Create oval sketch (40mm x 20mm)
    oval_sketch = (
        cq.Workplane("XY")
        .moveTo(oval_x, oval_y)
        .ellipse(40.0, 20.0, forConstruction=False)
    )
    # Perform a shallow groove cut
    result = result.faces("-Z").workplane().moveTo(oval_x, oval_y).ellipse(40.0, 20.0).cutBlind(-15.0)

# Ensure result is a valid Workplane/Shape
if not isinstance(result, (cq.Workplane, cq.Shape)):
    result = base.faces("+Z").workplane()

result = result.val()
