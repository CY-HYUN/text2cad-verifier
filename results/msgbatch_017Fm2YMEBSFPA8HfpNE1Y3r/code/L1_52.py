import cadquery as cq
import math

# Create a new workplane
result = cq.Workplane("XY")

# Draw a center rectangle 120.0 x 50.0 in the XY plane and extrude 6.0
result = result.rect(120.0, 50.0).extrude(6.0)

# Select the top surface for a sketch
result = result.faces(">Z").workplane()

# Create a slot/obround: total length 80.0, width 18.0, centered at origin, along X-axis
slot_length = 80.0
slot_width = 18.0
slot_half_length = slot_length / 2 - slot_width / 2

# Create the slot using a construction approach
result = result.sketch()

# Draw obround/slot centered at origin along X-axis using the sketch API
# Create the slot shape using rect and circle operations
# Left semicircle
result = result.circle(slot_width / 2, mode='s').moveTo(-slot_half_length, 0)
# Right semicircle  
result = result.circle(slot_width / 2, mode='a').moveTo(slot_half_length, 0)
# Rectangle in the middle
result = result.rect(slot_length - slot_width, slot_width, mode='a').moveTo(0, 0)

# Exit the sketch and perform an extruded cut through
result = result.finalize()
result = result.cutThruAll()

# Apply fillet with radius 4.0 to the four outer corners
# Select the edges at the top corners
result = result.edges("|Z").fillet(4.0)
