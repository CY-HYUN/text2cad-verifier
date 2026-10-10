import cadquery as cq
import math

# Create the base rectangular plate
# Center at origin on the bottom surface
# X: 120mm, Y: 50mm, Z: 6mm (in positive Z direction)
base_plate = cq.Workplane("XY").box(120, 50, 6, centered=True)

# Apply fillets to the four top edges (rounded corners)
# Get the edges that are at the top of the box
base_plate = base_plate.edges("|Z").fillet(4)

# Create the long oval slot
# The slot is centered at origin, runs along X-axis
# Total length: 80mm, width: 18mm (radius 9mm)
# Create an oval profile: two semicircles (radius 9mm) connected by two parallel lines
# Then extrude it through the thickness

# Create a 2D oval profile centered at origin
# The slot goes from -40 to +40 in X direction (total 80mm)
# The slot width is 18mm (so ±9mm in Y direction)

# Create the oval as a profile that can be extruded
slot_profile = (
    cq.Workplane("XY")
    .moveTo(-40, 0)  # Start at left end center
    .lineTo(-40, 9)  # Right side of left semicircle
    .radiusArc((40, 9), 9)  # Top arc connecting the two semicircles
    .lineTo(40, 0)  # Right end
    .lineTo(40, -9)  # Left side of right semicircle
    .radiusArc((-40, -9), 9)  # Bottom arc
    .close()
)

# Create the slot by cutting the profile through the plate
# We need to extrude the profile in Z direction to cut through
slot = slot_profile.extrude(6)

# Subtract the slot from the base plate
result = base_plate.cut(slot)
