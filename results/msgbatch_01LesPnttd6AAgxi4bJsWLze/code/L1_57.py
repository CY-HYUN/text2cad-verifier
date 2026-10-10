import cadquery as cq

# Create the main rectangular blank: 80x60x30 mm, centered at bottom surface
# Centered at bottom means centered in X and Y, with Z from 0 to 30
blank = cq.Workplane("XY").box(80, 60, 30, centered=[True, True, False])

# The blank is centered at (0, 0) in XY plane and goes from Z=0 to Z=30
# We need to remove a rectangular block from the upper right rear corner
# The removed block: 50x30x20 mm
# The corner of the removed block is at (40, 30, 30)
# This means the block extends from:
# X: 40 - 50 = -10 to 40 (but we need to align with outer surface)
# Actually, if corner is at (40, 30, 30) and block is 50x30x20:
# The block should be positioned so its corner (the inner corner of the notch) is at (40, 30, 30)
# Since the blank goes from -40 to 40 in X and -30 to 30 in Y
# The removed block goes from 15 to 40 in X, 0 to 30 in Y, and 10 to 30 in Z

# Let me reconsider: the outer side aligns with +X, +Y, +Z surfaces
# Blank: X from -40 to 40, Y from -30 to 30, Z from 0 to 30
# Removed block dimensions: 50x30x20
# The corner at (40, 30, 30) is the inner corner of the notch
# So the removed block goes from:
# X: 40-50 = -10 to 40
# Y: 30-30 = 0 to 30  
# Z: 30-20 = 10 to 30

# Create the cutout block
cutout = cq.Workplane("XY").box(50, 30, 20, centered=False).translate((-10, 0, 10))

# Subtract the cutout from the blank
result = blank.cut(cutout)

# Apply a fillet of 4mm to the inner corner of the L-shape
# The inner corner is where the vertical and horizontal parts meet
# This is at the base of the notch, which is the edge at X=-10, Y=0-30, Z=10
# We need to fillet the edges that form the inner corner

# Find and fillet the appropriate edges
# The inner corner edges are where the two perpendicular surfaces of the notch meet
result = result.edges("not on surface or on surface").fillet(4)

