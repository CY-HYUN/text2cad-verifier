import cadquery as cq
import math

# Create the main cylinder
# Diameter: 40mm, Length: 80mm (along Z-axis)
cylinder = cq.Workplane("XY").cylinder(height=80, radius=20, centered=True)

# Create the keyway (rectangular groove)
# Dimensions: 40mm long (along Z), 10mm wide (along Y), 5mm deep (radial, along X)
# The keyway is cut axially along the side of the cylinder

# Create a box for the keyway
# Position it so it cuts into the cylinder from the side
keyway = cq.Workplane("XY").box(
    length=10,      # width along Y-axis
    width=5,        # depth along X-axis (radial depth)
    height=40,      # length along Z-axis
    centered=True
)

# Translate the keyway box to the edge of the cylinder
# The cylinder has radius 20mm, we want to cut 5mm deep
# So we position the keyway at X = 20 - 5/2 = 17.5 (so it goes from radius 15 to 20)
keyway = keyway.translate((17.5, 0, 0))

# Subtract the keyway from the cylinder
result = cylinder.cut(keyway)
