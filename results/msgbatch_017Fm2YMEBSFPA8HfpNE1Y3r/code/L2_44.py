import cadquery as cq
import math

# Create the base plate (60x60x10mm)
base = cq.Workplane("XY").box(60, 60, 10, centered=True)

# Fin dimensions
fin_length = 60  # Along Y-axis
fin_thickness = 2  # Along X-axis
fin_height = 40  # Along Z-axis
base_width = 60  # Along X-axis

# Calculate spacing for 10 fins across 60mm base width
spacing = base_width / 9  # 9 gaps for 10 fins

# Create fins and combine with base
result = base

# Create 10 fins distributed along X-axis
for i in range(10):
    x_pos = -30 + i * spacing
    fin = (cq.Workplane("XY")
           .workplane(offset=5)  # Top surface of base plate
           .moveTo(x_pos, 0)  # Center along Y
           .rect(fin_thickness, fin_length)
           .extrude(fin_height))
    result = result.union(fin)
