import cadquery as cq
import math

# Create the main cuboid body
# Origin at center of bottom surface
# Dimensions: 90 (X) × 50 (Y) × 30 (Z)
result = cq.Workplane("XY").box(90, 50, 30, centered=True)

# Create the through slot in the center of the top surface
# Slot dimensions: 90mm (X) × 20mm (Y) × 12mm (depth in Z)
# The slot is centered on the top surface

# Create a box to cut out for the slot
# Positioned at the top surface, centered
slot_box = cq.Workplane("XY").box(90, 20, 12, centered=True)

# Move the slot box to the top surface
# The main body goes from Z = -15 to Z = 15 (height 30, centered)
# We want to cut from Z = 15 down 12mm, so center at Z = 15 - 6 = 9
slot_box = slot_box.translate((0, 0, 9))

# Cut the slot from the main body
result = result.cut(slot_box)

# Add fillets to the slot bottom and side walls
# We need to fillet the two long edges where the slot bottom meets the side walls
# These edges run along the X-axis at the bottom of the slot

# The edges to fillet are at:
# 1. Y = -10 (left side of slot), Z = 3 (bottom of slot after cutting)
# 2. Y = +10 (right side of slot), Z = 3 (bottom of slot after cutting)

# Use the edges function to select and fillet
# Get edges that are parallel to X-axis and at the slot bottom corners
result = result.edges("not >Y").fillet(2)

result = result
