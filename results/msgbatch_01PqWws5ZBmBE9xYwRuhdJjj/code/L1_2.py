import cadquery as cq
import math

# Create a new workplane on the XZ plane
wp = cq.Workplane("XZ")

# Create the profile for the revolved shape
# The profile is drawn in the XZ plane where X is the radius and Z is the axial direction
profile = (
    wp
    .moveTo(12.5, 0)      # Start at inner radius, bottom
    .lineTo(20.0, 0)      # Outer radius, bottom
    .lineTo(20.0, 60.0)   # Outer radius, middle height
    .lineTo(20.0, 60.0)   # Stay at same point (will add fillet here)
    .lineTo(20.0, 120.0)  # Outer radius, top
    .lineTo(12.5, 120.0)  # Inner radius, top
    .lineTo(12.5, 0)      # Back to start (inner radius, bottom)
    .close()
)

# Apply fillet at the step corner (at Z=60)
# We need to create the profile with a fillet at the corner
profile = (
    wp
    .moveTo(12.5, 0)
    .lineTo(20.0, 0)
    .lineTo(20.0, 60.0)
    .tangentArcPointToPoint((20.0, 60.0 + 3.0), relative=False)
    .lineTo(20.0, 120.0)
    .lineTo(12.5, 120.0)
    .lineTo(12.5, 0)
    .close()
)

# Create a simpler approach with proper fillet
# Draw the profile step by step
profile = (
    wp
    .moveTo(12.5, 0)
    .lineTo(20.0, 0)
    .lineTo(20.0, 60.0 - 3.0)
    .arc((20.0, 60.0 + 3.0), 3.0)  # Add 3mm fillet at corner
    .lineTo(20.0, 120.0)
    .lineTo(12.5, 120.0)
    .lineTo(12.5, 0)
    .close()
)

# Perform revolve operation around the Z-axis (centerline)
# The revolve uses the Y-axis as the revolution axis in the default orientation
# but since we're working in XZ plane, we need to revolve around Z
result = profile.revolve(360, (0, 0, 1), (0, 0, 0))
