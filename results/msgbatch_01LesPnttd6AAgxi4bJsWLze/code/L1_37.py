import cadquery as cq
import math

# Create the main circular disc
disc = cq.Workplane("XY").cylinder(radius=40, height=15)

# Create the cross-shaped slot
# The slot consists of two rectangular cutouts perpendicular to each other
# Each slot is 10mm wide and 5mm deep (but goes through from top)
# They extend from center to edge (radius 40mm)

# First, create a box for the X-direction slot (length along X-axis)
# It should be 80mm long (full diameter), 10mm wide (Y-direction), and 5mm deep (Z-direction)
slot_x = cq.Workplane("XY").box(80, 10, 5)

# Second, create a box for the Y-direction slot (length along Y-axis)
# It should be 10mm wide (X-direction), 80mm long (full diameter), and 5mm deep (Z-direction)
slot_y = cq.Workplane("XY").box(10, 80, 5)

# Combine the two slots into one cross shape
cross_slot = slot_x.union(slot_y)

# Position the cross slot at the top surface of the disc (Z = 5mm to center it at top)
# The disc has height 15mm, so top surface is at Z = 7.5mm
# We want the 5mm deep slot to cut into the top, so position it at Z = 5mm
cross_slot = cross_slot.translate((0, 0, 5))

# Cut the cross slot from the disc
result = disc.cut(cross_slot)
