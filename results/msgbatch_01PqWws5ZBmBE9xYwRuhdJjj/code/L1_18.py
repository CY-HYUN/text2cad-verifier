import cadquery as cq
import math

# Create a new workplane on the XZ plane
wp = cq.Workplane("XZ")

# Start at the origin and draw the capsule cross-section profile
# The profile consists of:
# 1. A vertical line segment at radius 15mm, extending 60mm along X
# 2. Two semicircular arcs at the ends with radius 15mm

# Start at one end of the capsule (x=0, z=15)
# Draw vertical line up to z=15
profile = (
    wp
    .moveTo(0, 15)  # Start at (x=0, z=15) in XZ plane
    .lineTo(60, 15)  # Line to (x=60, z=15) - 60mm long straight segment at radius 15mm
    .radiusArc((60, -15), 15)  # Arc from (60, 15) to (60, -15) with radius 15mm
    .lineTo(0, -15)  # Line from (60, -15) to (0, -15)
    .radiusArc((0, 15), 15)  # Arc from (0, -15) to (0, 15) with radius 15mm
    .close()  # Close the profile
)

# Revolve the profile 360 degrees around the X-axis
result = profile.revolve(360, (1, 0, 0))
