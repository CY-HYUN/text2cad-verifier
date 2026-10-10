import cadquery as cq
import math

# Create the profile for revolution around the Y-axis
# Build outer profile points
profile_points = []

# Start at origin
profile_points.append((0, 0))

# Vertical line from (100, 0) to (100, 50)
profile_points.append((100, 0))
profile_points.append((100, 50))

# Quarter-ellipse from (100, 50) to (0, 100)
# Center at (0, 50), major axis 100mm (horizontal), minor axis 50mm (vertical)
for angle in range(1, 91):
    t = math.radians(angle)
    x = 100 * math.cos(t)
    y = 50 + 50 * math.sin(t)
    profile_points.append((x, y))

# Back to origin along centerline
profile_points.append((0, 100))
profile_points.append((0, 0))

# Create the main body by revolving the profile
main_body = cq.Workplane("XY").polyline(profile_points).close().revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))

# Create the nozzle at the top
# Transform to top of the head (z=100) and create a ring
nozzle = (
    cq.Workplane("XY")
    .transformed(offset=(0, 100, 0))
    .circle(20)  # Outer radius (diameter 40mm)
    .hole(15)    # Inner hole radius (diameter 30mm)
    .extrude(30) # Extrude outward by 30mm
)

# Combine main body and nozzle
result = main_body.union(nozzle)
