import cadquery as cq
import math

# Create the base sketch on the XZ plane for the dished head profile
sketch = cq.Workplane("XZ")

# Draw the quarter-elliptical arc (semi-major axis = 100, semi-minor axis = 50)
# The arc goes from (0, 50) to (100, 0)
arc_points = []
for t in range(0, 91):
    angle = math.radians(t)
    x = 100 * math.sin(angle)
    z = 50 * math.cos(angle)
    arc_points.append((x, z))

# Create the profile as a wire
points = []
# Start from the top of the arc
points.append((0, 50))

# Add elliptical arc points
for point in arc_points[1:]:
    points.append(point)

# Draw vertical line downward from (100, 0) by 25 mm
points.append((100, -25))

# Create offset profile (inward by 8 mm)
offset_arc_points = []
for t in range(0, 91):
    angle = math.radians(t)
    x = (100 - 8) * math.sin(angle)
    z = (50 - 8) * math.cos(angle)
    offset_arc_points.append((x, z))

# Add the vertical line at the bottom (offset inward)
points.append((92, -25))

# Add the inner vertical line going up
points.append((92, -17))

# Add the reversed inner elliptical arc points
for point in reversed(offset_arc_points[1:]):
    points.append(point)

# Close back to start
points.append((0, 50))

# Create a sketch on XZ plane and draw the profile
sketch = cq.Workplane("XZ").polyline(points).close()

# Revolve the profile 360 degrees around the Y-axis
dished_head = sketch.revolve(360, axis=(0, 1, 0), clean=True)

# Create the nozzle boss at the top
# Find the top surface and create a sketch on it
nozzle_workplane = dished_head.faces(">Z").workplane()
nozzle_sketch = nozzle_workplane.circle(20)
boss = nozzle_sketch.extrude(30)

# Combine the dished head with the boss
result = dished_head.union(boss)
