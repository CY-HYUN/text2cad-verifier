import cadquery as cq

# Create the base rectangular prism
# Dimensions: 50mm wide (Y), 30mm high (Z), 100mm long (X)
base = cq.Workplane("XY").box(100, 50, 30)

# Create the groove to be removed
# Dimensions: 30mm wide (Y), 20mm high (Z), 100mm long (X)
# Positioned at the top center of the base
groove = cq.Workplane("XY").box(100, 30, 20).translate((0, 0, 5))

# Subtract the groove from the base to create the C-shaped cross-section
result = base.cut(groove)
