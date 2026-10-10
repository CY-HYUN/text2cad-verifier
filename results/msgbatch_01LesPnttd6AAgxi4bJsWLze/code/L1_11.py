import cadquery as cq
import math

# Create the main cylinder
# Diameter: 60mm, Height: 40mm
main_cylinder = cq.Workplane("XY").cylinder(height=40, radius=30, centered=True)

# Create the hole cylinder
# Diameter: 10mm (radius 5mm), offset 15mm from center, through-hole (height > main height)
# The hole is offset in the XY plane by 15mm from the center
hole = cq.Workplane("XY").workplane(offset=-20).cylinder(height=50, radius=5, centered=False).translate((15, 0, 0))

# Subtract the hole from the main cylinder
result = main_cylinder.cut(hole)
