import cadquery as cq
import math

# Create the base plate
base = cq.Workplane("XY").box(60, 60, 10)

# Create the fins
# 10 fins, each 60mm long (Y-axis), 40mm high (Z-axis), 2mm thick (X-axis)
# 4mm spacing between fins

# Calculate fin positions
# Total width needed for 10 fins of 2mm each with 4mm spacing between them
# 10 * 2mm + 9 * 4mm = 20 + 36 = 56mm (fits within 60mm base)

# Start position (centered)
start_x = -28  # This centers the fins on the 60mm width

fins = cq.Workplane("XY")

for i in range(10):
    # X position of each fin center
    x_pos = start_x + i * 6  # 2mm fin + 4mm gap = 6mm spacing
    
    # Create a fin: 60mm long (Y), 40mm high (Z), 2mm thick (X)
    # Position it so the bottom of the fin sits on top of the base
    fin = (cq.Workplane("XY")
           .box(2, 60, 40, centered=True)
           .translate((x_pos, 0, 20)))  # 10 + 40/2 = 30mm total height center
    
    fins = fins.union(fin)

# Combine base and fins
result = base.union(fins)
