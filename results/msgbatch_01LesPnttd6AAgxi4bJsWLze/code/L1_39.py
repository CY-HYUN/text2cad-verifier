import cadquery as cq

# Create the rectangular prism part (60mm long x 40mm wide x 10mm thick)
rect_prism = cq.Workplane("XY").box(60, 40, 10)

# Create the half-cylinder part
# The half-cylinder has diameter 40mm (radius 20mm), length 40mm (to match width)
# It should be positioned to the right of the rectangular prism
# A half-cylinder in CadQuery can be created by taking a cylinder and cutting it in half

# First, create a full cylinder with radius 20mm and height 40mm (along Y-axis)
cylinder = cq.Workplane("XY").cylinder(40, 20, centered=True)

# Create a box to use as a cutting tool - this will cut the cylinder in half
# The box extends in the Z direction to cut everything below Z=0
cutting_box = cq.Workplane("XY").box(100, 100, 10, centered=True)
cutting_box = cutting_box.translate((0, 0, -10))

# Create half-cylinder by cutting the cylinder
half_cylinder = cylinder.cut(cutting_box)

# Position the half-cylinder to the right of the rectangular prism
# The rectangular prism extends from -30 to +30 in X (60mm total, centered)
# The half-cylinder should start where the prism ends (at X=30)
# and extend to X=30+40=70 (but we need to position its center at X=50)
half_cylinder = half_cylinder.translate((50, 0, 0))

# Union the rectangular prism and half-cylinder
result = rect_prism.union(half_cylinder)
