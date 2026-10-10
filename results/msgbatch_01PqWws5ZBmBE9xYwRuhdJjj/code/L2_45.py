import cadquery as cq
import math

# Create a 2D profile in the XY plane (front view)
# We'll create the outer wavy profile and then revolve it

# Parameters
centerline_length = 100
crest_radius = 22.5
trough_radius = 17.5
wavelength = 10
num_waves = 10
wall_thickness = 2
num_points = num_waves * 20  # More points for smoother wave

# Create the outer wavy profile
points = []

# Generate wavy profile along the centerline
for i in range(num_points + 1):
    z = (centerline_length / num_points) * i
    # Alternate between crest and trough
    t = (i / num_points) * num_waves * 2 * math.pi
    radius = crest_radius + (trough_radius - crest_radius) * (math.cos(t) + 1) / 2
    points.append((radius, z))

# Create a sketch for the outer profile
sketch_outer = cq.Sketch()
sketch_outer.polyline(points)

# Create the inner wavy profile (offset inward by wall thickness)
inner_points = []
for i in range(num_points + 1):
    z = (centerline_length / num_points) * i
    t = (i / num_points) * num_waves * 2 * math.pi
    radius = crest_radius + (trough_radius - crest_radius) * (math.cos(t) + 1) / 2
    inner_radius = radius - wall_thickness
    inner_points.append((inner_radius, z))

# Create closed profile by combining outer and inner profiles
# Start from bottom of outer profile
profile_points = []

# Add outer profile (bottom to top)
for i in range(len(points)):
    profile_points.append(points[i])

# Add top cap
profile_points.append((inner_points[-1][0], inner_points[-1][1]))

# Add inner profile (top to bottom, reversed)
for i in range(len(inner_points) - 1, -1, -1):
    profile_points.append(inner_points[i])

# Close the profile
profile_points.append((points[0][0], points[0][1]))

# Create a workplane and sketch the profile
wp = cq.Workplane("XZ")
sketch = wp.sketch()
sketch.polyline(profile_points)
sketch.close()

# Create the 2D face
face = wp.finalize().wires.objects[0].getWire()

# Use revolve to create the 3D corrugated pipe
# We need to work in the right coordinate system
# Create on XZ plane and revolve around Z axis
wp = cq.Workplane("XZ").polyline(profile_points).close()

# Revolve around the Z axis (360 degrees)
result = wp.revolve(360, (0, 0, 0), (0, 0, 1))
