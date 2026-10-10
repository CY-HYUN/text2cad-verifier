import cadquery as cq
import math

# Parameters
centerline_length = 100
crest_radius = 22.5
trough_radius = 17.5
wavelength = 10
num_waves = 10
wall_thickness = 2
num_points = num_waves * 20  # More points for smoother wave

# Generate outer wavy profile points
outer_points = []
for i in range(num_points + 1):
    z = (centerline_length / num_points) * i
    t = (i / num_points) * num_waves * 2 * math.pi
    radius = crest_radius + (trough_radius - crest_radius) * (math.cos(t) + 1) / 2
    outer_points.append((radius, z))

# Generate inner wavy profile points (offset inward by wall thickness)
inner_points = []
for i in range(num_points + 1):
    z = (centerline_length / num_points) * i
    t = (i / num_points) * num_waves * 2 * math.pi
    radius = crest_radius + (trough_radius - crest_radius) * (math.cos(t) + 1) / 2
    inner_radius = radius - wall_thickness
    inner_points.append((inner_radius, z))

# Create closed profile by combining outer and inner profiles
profile_points = []

# Add outer profile (bottom to top)
for point in outer_points:
    profile_points.append(point)

# Add inner profile (top to bottom, reversed)
for point in reversed(inner_points):
    profile_points.append(point)

# Close the profile by returning to start
profile_points.append(outer_points[0])

# Create a workplane on XZ plane and draw the closed profile
wp = cq.Workplane("XZ")

# Draw the profile as a polyline
for i, point in enumerate(profile_points):
    if i == 0:
        wp = wp.moveTo(point[0], point[1])
    else:
        wp = wp.lineTo(point[0], point[1])

# Create a face from the profile
wp = wp.close()

# Revolve around the Z axis (360 degrees)
result = wp.revolve(360, (0, 0, 0), (0, 0, 1))
