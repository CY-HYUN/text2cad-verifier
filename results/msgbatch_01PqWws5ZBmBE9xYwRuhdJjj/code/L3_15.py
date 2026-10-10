import cadquery as cq
import math

# Create the base sketch on the XZ plane for the dished head profile
sketch = cq.Workplane("XZ").center(0, 0)

# Draw the quarter-elliptical arc (semi-major axis = 100, semi-minor axis = 50)
# The arc goes from (0, 50) to (100, 0)
arc_points = []
for t in range(0, 91):
    angle = math.radians(t)
    x = 100 * math.sin(angle)
    z = 50 * math.cos(angle)
    arc_points.append((x, z))

# Start from the top of the arc
sketch = sketch.moveTo(0, 50)

# Draw the elliptical arc
for point in arc_points[1:]:
    sketch = sketch.lineTo(point[0], point[1])

# Draw vertical line downward from (100, 0) by 25 mm
sketch = sketch.lineTo(100, -25)

# Create offset profile (inward by 8 mm)
# For the offset, we need to go inward from the ellipse and the vertical line
offset_arc_points = []
for t in range(0, 91):
    angle = math.radians(t)
    x = (100 - 8) * math.sin(angle)
    z = (50 - 8) * math.cos(angle)
    offset_arc_points.append((x, z))

# Draw the inner vertical line (offset inward)
sketch = sketch.lineTo(92, -25)
sketch = sketch.lineTo(92, -25 + 8)

# Draw the inner elliptical arc (reverse direction)
for point in reversed(offset_arc_points[1:]):
    sketch = sketch.lineTo(point[0], point[1])

# Close the profile by drawing a line from inner arc top to outer arc top
sketch = sketch.lineTo(0, 50)

# Complete the profile
profile = sketch.close()

# Revolve the profile 360 degrees around the Y-axis (vertical)
dished_head = profile.revolve(360, (0, 1, 0))

# Get the top of the dished head (at the apex)
# The apex is at approximately z = 50
# Create a tangent plane at the apex
tangent_plane = dished_head.faces(">Z").first()

# Switch to the top face to create the nozzle boss
nozzle_sketch = cq.Workplane("XY").center(0, 50)

# Draw two concentric circles: outer diameter 40 mm, inner diameter 30 mm
# We'll draw them as a sketch with two circles
nozzle_sketch = nozzle_sketch.circle(20)  # Outer circle, radius 20 mm
nozzle_sketch = nozzle_sketch.circle(15)  # Inner circle, radius 15 mm

# Create the annular face and extrude upward by 30 mm
# First, create a simple circular boss
boss_sketch = cq.Workplane("XY").center(0, 50)
boss_sketch = boss_sketch.circle(20)
boss = boss_sketch.extrude(30)

# Combine the dished head with the boss
result = dished_head.union(boss)
