import cadquery as cq

# Create the vertical part (standing up in Z direction)
# 40mm wide (Y), 10mm thick (X), 60mm high (Z)
vertical = cq.Workplane("XY").box(10, 40, 60)

# Create the horizontal part (extending in X direction)
# 50mm long (X), 40mm wide (Y), 10mm thick (Z)
horizontal = cq.Workplane("XY").box(50, 40, 10)

# Position the horizontal part so it connects at the bottom of the vertical part
# The horizontal part should be at Z = -5 (half its thickness below the vertical part's base)
# and aligned so they overlap properly at the corner
horizontal = horizontal.translate((25, 0, -5))

# Position the vertical part at the corner
# The vertical part should have its base at Z = -30 (so it extends from -30 to 30)
# and positioned so its back edge aligns with the X=0 plane
vertical = vertical.translate((5, 0, 0))

# Create the L-shaped structure by unioning the two parts
result = vertical.union(horizontal)
