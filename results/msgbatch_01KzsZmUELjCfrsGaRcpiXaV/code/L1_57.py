import cadquery as cq

# Create the main rectangular blank: 80x60x30 mm, centered at bottom surface
# Centered at bottom means centered in X and Y, with Z from 0 to 30
blank = cq.Workplane("XY").box(80, 60, 30, centered=[True, True, False])

# The blank extends from:
# X: -40 to 40, Y: -30 to 30, Z: 0 to 30

# Remove a rectangular block from the upper right rear corner
# Removed block: 50x30x20 mm
# The inner corner of the notch is at (40, 30, 30)
# So the block extends from X: -10 to 40, Y: 0 to 30, Z: 10 to 30

cutout = cq.Workplane("XY").box(50, 30, 20, centered=False).translate((-10, 0, 10))

# Subtract the cutout from the blank
result = blank.cut(cutout)

# Apply a fillet of 4mm to the inner corner edges of the L-shape
# These are the edges at the base of the notch where the cut surfaces meet
# We select edges by filtering based on their location
result = result.edges("|Z").filter(lambda e: e.endPoint.z == 10).fillet(4)

