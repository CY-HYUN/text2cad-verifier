import cadquery as cq
import math

# Create the main cylinder
main_cylinder = cq.Workplane("XY").cylinder(height=80, radius=25)

# Create the annular groove
# The groove is at the midpoint (z=0 when centered), 10mm wide, 5mm deep
# We'll create a rectangular profile and revolve it around the Z-axis

# Start with a sketch on the XZ plane to define the groove profile
# The groove profile is a rectangle: 10mm wide (in Z direction), 5mm deep (in radial direction)
groove_profile = (
    cq.Workplane("XZ")
    .rect(10, 5)  # 10mm wide in Z, 5mm deep in radial direction
    .revolve(360, axisEnd=(0, 0, 1))  # Revolve around Z-axis
)

# Position the groove profile correctly
# The groove should be at z=0 (middle of cylinder)
# The groove should cut inward 5mm from the outer surface (radius 25)
# So it should be at radius 20 (25-5)

# Create groove by defining the cut path
# We'll use a different approach: create a cutting tool
groove_cutter = (
    cq.Workplane("XY")
    .moveTo(20, 0)  # Start at radius 20 (25-5)
    .rect(5, 10, centered=True)  # 5mm radial depth, 10mm height
    .revolve(360)
)

# Subtract the groove from the main cylinder
result = main_cylinder.cut(groove_cutter)
