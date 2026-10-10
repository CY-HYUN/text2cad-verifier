import cadquery as cq

# Create the vertical plate on the YZ plane
# The plate is 40.0 mm wide (Y direction) and 60.0 mm high (Z direction)
# Extrude 10.0 mm along +X direction
vertical_plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(10.0, 40.0)  # Width in X (extrusion thickness), Height in Y (width)
    .extrude(60.0)  # Extrude in Z direction for height
)

# Reposition the vertical plate to be on YZ plane
# We need to create it differently - sketch on YZ plane
vertical_plate = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .rect(40.0, 60.0)  # Width (Y) and height (Z)
    .extrude(10.0)  # Extrude 10.0 mm along +X direction
)

# Create the horizontal plate on the XY plane
# The plate is 50.0 mm long (X direction) and 40.0 mm wide (Y direction)
# Extrude 10.0 mm along +Z direction
horizontal_plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(50.0, 40.0)  # Length (X) and width (Y)
    .extrude(10.0)  # Extrude 10.0 mm along +Z direction
)

# Position the horizontal plate so its inner corner aligns with the bottom inner corner
# of the vertical plate. The vertical plate starts at Z=0 and goes to Z=60.
# We position the horizontal plate at Z=0 (bottom) and shift it to overlap correctly
# The vertical plate occupies X: 0 to 10, Y: -20 to 20 (centered), Z: 0 to 60
# The horizontal plate should start at X=0, Y=-20 (to align with vertical plate width)

# Recreate with proper positioning
vertical_plate = (
    cq.Workplane("YZ")
    .moveTo(0, 30)  # Center at Y=0, move up to Z=30 (height 60, so center is at 30)
    .rect(40.0, 60.0)  # Width 40mm (Y direction), Height 60mm (Z direction)
    .extrude(10.0)  # Extrude 10mm along +X
)

# Horizontal plate positioned to overlap at the bottom corner
horizontal_plate = (
    cq.Workplane("XY")
    .moveTo(25, -20)  # Center of plate: X=25 (length 50), Y=-20 (width 40, offset)
    .rect(50.0, 40.0)  # Length 50mm (X), Width 40mm (Y)
    .extrude(10.0)  # Extrude 10mm along +Z
)

# Perform Boolean union to create L-shaped bracket
result = vertical_plate.union(horizontal_plate)
