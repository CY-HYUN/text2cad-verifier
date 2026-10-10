import cadquery as cq
import math

# Create a new workplane
result = cq.Workplane("XY")

# Draw a center rectangle 120.0 x 50.0 in the XY plane and extrude 6.0
result = result.rect(120.0, 50.0).extrude(6.0)

# Select the top surface for a sketch
result = result.faces(">Z").workplane()

# Create a slot/obround: total length 80.0, width 18.0, centered at origin, along X-axis
# A slot is created by drawing a rectangle and using the slot tool
# We'll create it as a rectangle with rounded ends (obround shape)
slot_length = 80.0
slot_width = 18.0

# Create the slot as a rectangle with rounded ends using a path
slot_half_length = slot_length / 2 - slot_width / 2
result = result.sketch()

# Draw obround/slot centered at origin along X-axis
# Obround = rectangle with semicircles at the ends
result = result.moveTo(-slot_half_length, 0)
result = result.radiusArc((slot_half_length, 0), slot_width / 2)
result = result.lineTo(slot_half_length, slot_width / 2)
result = result.radiusArc((slot_half_length, -slot_width / 2), slot_width / 2)
result = result.lineTo(-slot_half_length, -slot_width / 2)
result = result.radiusArc((-slot_half_length, slot_width / 2), slot_width / 2)
result = result.close()

# Exit the sketch and perform an extruded cut through
result = result.finalize()
result = result.cutThruAll()

# Apply fillet with radius 4.0 to the four outer corners
# Select the vertical edges at the corners
result = result.edges("|Z").fillet(4.0)

