import cadquery as cq
import math

# Initialize and create base manifold block
base = cq.Workplane("XY").rect(200.0, 100.0).extrude(80.0)

# Drill three horizontal blind holes on front (XZ plane) at center height
# These are oil inlets at equal intervals
result = base.faces(">Y").workplane()
for x_pos in [-60.0, 0.0, 60.0]:
    result = result.moveTo(x_pos, 0).hole(20.0, 60.0)

# Create top surface distribution holes (two rows of five circles each)
result = result.faces(">Z").workplane()
# Row 1: 5 holes
for i in range(5):
    x_pos = -80.0 + i * 40.0
    y_pos = -20.0
    result = result.moveTo(x_pos, y_pos).hole(10.0, 50.0)

# Row 2: 5 holes
for i in range(5):
    x_pos = -80.0 + i * 40.0
    y_pos = 20.0
    result = result.moveTo(x_pos, y_pos).hole(10.0, 50.0)

# Add countersunk bolt holes at four corners of top surface
corners = [(-100.0, -50.0), (100.0, -50.0), (-100.0, 50.0), (100.0, 50.0)]
for corner_x, corner_y in corners:
    result = result.moveTo(corner_x, corner_y).hole(8.0, 80.0)

# Add countersinks for bolt holes on top surface
result = result.faces(">Z").workplane()
for corner_x, corner_y in corners:
    result = result.moveTo(corner_x, corner_y).cskHole(8.0, 12.0, 82.0, 2.0)

# Create oval grooves on bottom surface for weight reduction
result = result.faces("<Z").workplane()
oval_positions = [(-60.0, -25.0), (60.0, -25.0), (-60.0, 25.0), (60.0, 25.0)]

for oval_x, oval_y in oval_positions:
    # Create and cut oval groove
    sketch = cq.Workplane("XY").moveTo(oval_x, oval_y).ellipse(40.0, 20.0)
    result = result.cutBlind(-15.0)

result = result.val()
