import cadquery as cq
import math

# Create the base plate
base = cq.Workplane("XY").box(60, 60, 10)

# Create the fins
# 10 fins, each 60mm long (Y-axis), 40mm high (Z-axis), 2mm thick (X-axis)
# 4mm spacing between fins
# Total fin assembly width: 10 * 2mm + 9 * 4mm = 56mm

# Calculate fin positions to fit within 60mm base width
# Space them across the X-axis with 4mm gaps
start_x = -28  # Center position for first fin

fins = cq.Workplane("XY")

for i in range(10):
    # X position of each fin center
    x_pos = start_x + i * 6  # 2mm fin + 4mm gap = 6mm spacing
    
    # Create a fin: 2mm thick (X), 60mm long (Y), 40mm high (Z)
    # Position it so the bottom of the fin sits on top of the base (at Z = 10)
    # The fin extends 40mm upward from Z = 10 to Z = 50
    fin = (cq.Workplane("XY")
           .box(2, 60, 40, centered=True)
           .translate((x_pos, 0, 25)))  # 10 + 40/2 = 25mm for top of base + half fin height
    
    fins = fins.union(fin)

# Combine base and fins
result = base.union(fins)
