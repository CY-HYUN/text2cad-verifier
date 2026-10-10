import cadquery as cq
import math

# Create the base rectangular plate
# Center at origin on the bottom surface
# X: 120mm, Y: 50mm, Z: 6mm (in positive Z direction)
base_plate = cq.Workplane("XY").box(120, 50, 6, centered=True)

# Apply fillets to the four top edges (rounded corners)
# Get the edges that are at the top of the box
base_plate = base_plate.edges("|Z").fillet(4)

# Create the long oval slot using a different approach
# The slot is an oval with:
# - Total length: 80mm (so semi-major axis = 40mm along X)
# - Width: 18mm (so semi-minor axis = 9mm along Y)
# Create this as a 2D profile and extrude it to cut through

# Build the oval profile by creating a sketch
slot_profile = (
    cq.Workplane("XY")
    .moveTo(-40, 0)  # Start at left end center
    .lineTo(-40, 9)  # Move to top-left corner
    .threePointArc((-40, 9), (0, 9), (40, 9))  # Top curve
    .lineTo(40, 0)  # Right end center
    .lineTo(40, -9)  # Move to bottom-right corner
    .threePointArc((40, -9), (0, -9), (-40, -9))  # Bottom curve
    .close()
)

# Create the slot by extruding the profile
slot = slot_profile.extrude(6)

# Subtract the slot from the base plate
result = base_plate.cut(slot)
