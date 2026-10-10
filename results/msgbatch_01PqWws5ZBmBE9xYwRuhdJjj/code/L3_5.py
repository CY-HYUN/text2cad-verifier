import cadquery as cq
import math

# Create the main body (ellipsoidal head with straight edge)
# Start with Front plane and create a rotational sketch

# Create the profile for revolution
# The profile consists of:
# 1. A vertical line from (100, 0) to (100, 50)
# 2. A quarter-ellipse from (100, 50) to (0, 100)
# 3. Offset inward by 10mm
# 4. Closed profile

# Build the outer profile
outer_profile = (
    cq.Workplane("XY")
    .moveTo(100, 0)
    .lineTo(100, 50)  # Vertical line segment
)

# Add quarter-ellipse from (100, 50) to (0, 100)
# Center at (0, 50), major axis 100mm (horizontal), minor axis 50mm (vertical)
# We'll approximate with an arc or use parametric approach
# For a proper ellipse: x = a*cos(t), y = center_y + b*sin(t)
# where a=100, b=50, center=(0,50)
# At (100,50): cos(t)=1, sin(t)=0, so t=0
# At (0,100): cos(t)=0, sin(t)=1, so t=90°

# Using parametric ellipse
points_ellipse = []
for angle in range(0, 91, 5):
    t = math.radians(angle)
    x = 100 * math.cos(t)
    y = 50 + 50 * math.sin(t)
    points_ellipse.append((x, y))

# Build outer profile by adding ellipse points
for pt in points_ellipse[1:]:
    outer_profile = outer_profile.lineTo(pt[0], pt[1])

# Close back to origin along Y-axis
outer_profile = outer_profile.lineTo(0, 100).lineTo(0, 0).close()

# Now create the inner offset profile (10mm inward)
inner_profile = (
    cq.Workplane("XY")
    .moveTo(90, 0)
    .lineTo(90, 50)  # Offset vertical line
)

# Add offset quarter-ellipse
points_ellipse_inner = []
for angle in range(0, 91, 5):
    t = math.radians(angle)
    # Approximate offset by scaling down the ellipse
    x = 90 * math.cos(t)
    y = 50 + 40 * math.sin(t)
    points_ellipse_inner.append((x, y))

for pt in points_ellipse_inner[1:]:
    inner_profile = inner_profile.lineTo(pt[0], pt[1])

inner_profile = inner_profile.lineTo(0, 90).lineTo(0, 0).close()

# Create the closed section by combining outer and inner
section = outer_profile.moveTo(0, 0)

# Create the main body by revolving around Y-axis (vertical axis through origin)
main_body = (
    cq.Workplane("XY")
    .moveTo(100, 0)
    .lineTo(100, 50)
)

# Add the ellipse arc points
for angle in range(0, 91, 3):
    t = math.radians(angle)
    x = 100 * math.cos(t)
    y = 50 + 50 * math.sin(t)
    main_body = main_body.lineTo(x, y)

# Close the profile
main_body = main_body.lineTo(0, 0).close()

# Revolve around Y-axis (360 degrees)
main_body = main_body.revolve(axisEnd=(0, 1, 0), angleStart=0, angleDegree=360)

# Create the nozzle
# At the top vertex (0, 100), create a concentric ring
# Outer diameter 40mm, inner diameter 30mm, extrude 30mm outward

nozzle_sketch = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 100))
    .circle(20)  # Outer radius
    .circle(15)  # Inner radius (hole)
)

# Extrude outward (along Z direction)
nozzle = nozzle_sketch.extrude(30)

# Combine main body and nozzle
result = main_body.union(nozzle)
