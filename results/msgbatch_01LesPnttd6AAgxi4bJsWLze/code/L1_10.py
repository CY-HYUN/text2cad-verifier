import cadquery as cq

# Create the main cuboid body
main_body = cq.Workplane("XY").box(100, 50, 30)

# Create a rectangular slot on the upper surface
# The slot is 20mm wide (Y direction), 15mm deep (Z direction), and runs along the entire length (X direction)
# The slot is centered on the upper surface

# Define the slot as a rectangular cutout
# Slot dimensions: 100mm (length, X) x 20mm (width, Y) x 15mm (depth, Z)
# Position: centered in Y, starts from the top surface and goes down 15mm

slot = cq.Workplane("XY").box(100, 20, 15).translate((0, 0, 7.5))

# Subtract the slot from the main body
result = main_body.cut(slot)
