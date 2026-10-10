import cadquery as cq
import math

# Create the base plate (60x60x10mm)
base = cq.Workplane("XY").box(60, 60, 10, centered=True)

# Get the top face of the base plate
top_face = base.faces(">Z").first()

# Create the first fin sketch on the top edge
# The fin is 60x2mm, positioned at one edge of the base
# Start at the top face and sketch the fin
fin_sketch = (cq.Workplane("XY")
              .workplane(offset=10)  # Work on top surface of base plate
              .moveTo(-30, -30)  # Position at one edge
              .rect(60, 2)
              .extrude(40))  # Extrude to 40mm height

# Create fins using linear array
# We need 10 instances along the X-axis with spacing
# The base plate is 60mm wide, so spacing = 60/9 ≈ 6.67mm for 10 fins
# We'll create a single fin and use linear array to replicate it

# Start fresh with a better approach
# Create a workplane and build fins systematically
fin_width = 60  # X direction
fin_thickness = 2  # Y direction
fin_height = 40  # Z direction
base_width = 60

# Create the base plate
result = cq.Workplane("XY").box(60, 60, 10, centered=True)

# Calculate spacing for 10 fins across 60mm
spacing = base_width / 9  # 9 gaps for 10 fins

# Create a single fin
fin = (cq.Workplane("XY")
       .workplane(offset=5)  # Start at top of base (10/2 = 5mm up from center, then +10 to get to top)
       .moveTo(0, -29)  # Position at one edge (60/2 - 2/2 = 29 for Y)
       .rect(fin_width, fin_thickness)
       .extrude(fin_height, combine=False))

# Linear array the fin along X-axis
# Position fins from -30 to +30 with even spacing
fins_list = []
for i in range(10):
    x_pos = -30 + i * spacing
    fin_single = (cq.Workplane("XY")
                  .workplane(offset=5)
                  .moveTo(x_pos, -29)
                  .rect(fin_width, fin_thickness)
                  .extrude(fin_height))
    fins_list.append(fin_single)

# Combine all fins with the base
result = result.union(fins_list[0])
for fin in fins_list[1:]:
    result = result.union(fin)
