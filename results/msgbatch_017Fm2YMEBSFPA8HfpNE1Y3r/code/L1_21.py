import cadquery as cq
import math

# Create a new part with units in millimeters
# Start with a cylinder: diameter 50mm, height 80mm
cylinder = cq.Workplane("XY").circle(25).extrude(80)

# Create the annular groove on the XZ plane
# The groove profile is a rectangle: 5mm radial depth, 10mm axial width
# Centered at z=40mm (so from z=35 to z=45)
# Inner radius after cut: 25 - 5 = 20mm

# Create the groove profile as a rectangle on the XZ plane
# Position it so it extends from radius 20 to 25 (the outer surface)
groove_profile = (
    cq.Workplane("XZ")
    .rect(5, 10)  # width=5mm (radial), height=10mm (axial)
    .translate((22.5, 40, 0))  # center at radius 22.5, z=40
)

# Revolve the groove profile 360 degrees around the Z-axis
groove = groove_profile.revolve(360, (0, 0, 0), (0, 0, 1))

# Cut the groove from the cylinder to create the annular groove
result = cylinder.cut(groove)
