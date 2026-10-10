import cadquery as cq
import math

# Create the central pillar
pillar = cq.Workplane("XY").circle(10).extrude(100)

# Create the sector sketch for the step
# A sector is defined by inner radius, outer radius, and central angle
inner_radius = 5
outer_radius = 25
angle = 30

# Create a sketch for the sector on the bottom surface
sector_sketch = cq.Workplane("XY").moveTo(0, 0)

# Create sector using polygon approximation
# Convert angle to radians
angle_rad = math.radians(angle)

# Create the sector by drawing lines from center
points = [(0, 0)]

# Outer arc points
num_points = 20
for i in range(num_points + 1):
    t = i / num_points
    curr_angle = t * angle_rad
    x = outer_radius * math.cos(curr_angle)
    y = outer_radius * math.sin(curr_angle)
    points.append((x, y))

# Inner arc points (reversed)
for i in range(num_points, -1, -1):
    t = i / num_points
    curr_angle = t * angle_rad
    x = inner_radius * math.cos(curr_angle)
    y = inner_radius * math.sin(curr_angle)
    points.append((x, y))

# Close the polygon
points.append(points[0])

# Create the sector face
sector_face = cq.Workplane("XY").polyline(points).close().extrude(5)

# Create the spiral staircase by arraying the sector
result = pillar

for i in range(10):
    # Rotation angle for this instance (30 degrees per step)
    rotation_angle = i * 30
    # Height displacement for this instance (10mm per step)
    z_displacement = i * 10
    
    # Create a copy of the sector and apply transformations
    step = cq.Workplane("XY").moveTo(0, 0).polyline(points).close().extrude(5)
    
    # Apply rotation around Z-axis
    step = step.rotate((0, 0, 0), (0, 0, 1), rotation_angle)
    
    # Apply Z displacement
    step = step.translate((0, 0, z_displacement))
    
    # Union with the result
    result = result.union(step)

