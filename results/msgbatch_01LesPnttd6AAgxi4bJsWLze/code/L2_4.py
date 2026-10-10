import cadquery as cq
import math

# Create the base plate: 100x100mm, 15mm thick
base_plate = cq.Workplane("XY").box(100, 100, 15)

# Add fillets to the four corners of the base plate (R10mm)
base_plate = base_plate.edges("|Z").fillet(10)

# Create the central bearing sleeve: cylinder from center of base
# Outer diameter 60mm, inner diameter 40mm, height 40mm
# This is a hollow cylinder (ring)
bearing_outer = cq.Workplane("XY").circle(30).extrude(40)
bearing_inner = cq.Workplane("XY").circle(20).extrude(40)
bearing_sleeve = bearing_outer.cut(bearing_inner)

# Position the bearing sleeve at the top of the base plate
bearing_sleeve = bearing_sleeve.translate((0, 0, 15))

# Combine base plate and bearing sleeve
part = base_plate.union(bearing_sleeve)

# Create four through-holes at the corners in an 80x80mm square pattern
# Hole diameter: 10mm (radius 5mm)
# Pattern: 80x80mm square centered at origin
# Corners at: (±40, ±40)

hole_positions = [
    (40, 40),
    (40, -40),
    (-40, 40),
    (-40, -40)
]

for x, y in hole_positions:
    hole = cq.Workplane("XY").circle(5).extrude(15)
    hole = hole.translate((x, y, 0))
    part = part.cut(hole)

result = part
