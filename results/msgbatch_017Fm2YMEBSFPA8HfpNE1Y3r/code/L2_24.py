import cadquery as cq
import math

# Create profile points for revolution on XZ plane
# Profile will be revolved around Z axis to create the 3D shape

wp = cq.Workplane("XZ")

# Start creating the profile wire
profile_points = []

# Outer right edge going up: from (10, 0) to (10, 30)
profile_points.append((10, 0))
profile_points.append((10, 30))

# Inward passage at top: from (10, 30) to (5, 30)
profile_points.append((5, 30))

# Semicircle from (5, 30) down to (5, 0) with radius 15, center at (0, 15)
# Generate semicircle points
for i in range(17):
    angle = i * math.pi / 16  # 0 to pi radians
    x = 15 * math.cos(angle)
    y = 15 - 15 * math.sin(angle)  # Center at y=15
    profile_points.append((x, y))

# Close back to start
profile_points.append((10, 0))

# Create wire from points
wp = wp.moveTo(profile_points[0][0], profile_points[0][1])
for pt in profile_points[1:]:
    wp = wp.lineTo(pt[0], pt[1])

wp = wp.close()

# Revolve the profile 360 degrees around the Z axis to create the 3D solid
result = wp.revolve(360, (0, 0, 1))
