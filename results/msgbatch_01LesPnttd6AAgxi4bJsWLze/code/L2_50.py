import cadquery as cq
import math

# Create the base shaft with three cylindrical sections
# Start with the left section: diameter 40mm, length 30mm
shaft = cq.Workplane("XY").cylinder(30, 40/2)

# Add the middle section: diameter 30mm, length 40mm
# Position it at x = 30 (end of left section)
shaft = shaft.union(
    cq.Workplane("XY").transformed(offset=(30, 0, 0)).cylinder(40, 30/2)
)

# Add the right section: diameter 20mm, length 30mm
# Position it at x = 70 (end of middle section)
shaft = shaft.union(
    cq.Workplane("XY").transformed(offset=(70, 0, 0)).cylinder(30, 20/2)
)

# Add the keyway on top of the middle section
# Keyway: 20mm long, 6mm wide, 3.5mm deep
# The middle section is centered at x=50 (30 + 40/2), so keyway extends from x=40 to x=60
# We create a rectangular box and cut it from the shaft
keyway_box = cq.Workplane("XY").box(20, 6, 3.5, centered=True)
keyway_box = keyway_box.translate((50, 15, 0))  # Position at top of middle section

shaft = shaft.cut(keyway_box)

# Add center holes at each end face
# Left end: diameter 5mm, depth 10mm (goes into the left section from x=0)
left_hole = cq.Workplane("XY").cylinder(10, 5/2)
shaft = shaft.cut(left_hole)

# Right end: diameter 5mm, depth 10mm (goes into the right section from x=100)
right_hole = cq.Workplane("XY").transformed(offset=(100, 0, 0)).cylinder(10, 5/2)
shaft = shaft.cut(right_hole)

result = shaft
