import cadquery as cq
import math

# Create a new workplane on the XZ plane
wp = cq.Workplane("XZ")

# Start at the origin and draw the capsule cross-section profile
# The profile consists of a rectangle with semicircular caps on the ends
# We'll draw it as a closed spline/wire that can be properly revolved

# Draw the capsule profile in the XZ plane:
# Start at bottom left, go up, arc right, down, arc left back to start
profile = (
    wp
    .moveTo(0, -15)  # Start at (x=0, z=-15)
    .lineTo(0, 15)   # Vertical line up to (x=0, z=15)
    .radiusArc((60, 15), 15)  # Arc to (x=60, z=15) with radius 15
    .lineTo(60, -15)  # Vertical line down to (x=60, z=-15)
    .radiusArc((0, -15), 15)  # Arc back to (x=0, z=-15) with radius 15
    .close()  # Close the profile
)

# Revolve the profile 360 degrees around the X-axis
result = profile.revolve(360, (1, 0, 0))
