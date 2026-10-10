import cadquery as cq

# Create the vertical plate on the YZ plane
# The plate is 40.0 mm wide (Y direction) and 60.0 mm high (Z direction)
# Extrude 10.0 mm along +X direction
vertical_plate = (
    cq.Workplane("YZ")
    .moveTo(0, 30)  # Center at Y=0, move up to Z=30 (height 60, so center is at 30)
    .rect(40.0, 60.0)  # Width 40mm (Y direction), Height 60mm (Z direction)
    .extrude(10.0)  # Extrude 10mm along +X
)

# Create the horizontal plate on the XY plane
# The plate is 40.0 mm long (X direction) and 40.0 mm wide (Y direction)
# Extrude 10.0 mm along +Z direction
horizontal_plate = (
    cq.Workplane("XY")
    .moveTo(20, 0)  # Center of plate: X=20 (length 40), Y=0 (centered on width 40)
    .rect(40.0, 40.0)  # Length 40mm (X), Width 40mm (Y)
    .extrude(10.0)  # Extrude 10mm along +Z
)

# Perform Boolean union to create L-shaped bracket
result = vertical_plate.union(horizontal_plate)
