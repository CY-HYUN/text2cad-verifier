import cadquery as cq
import math

# Create the base plate: 100x100mm, 15mm thick
base_plate = cq.Workplane("XY").box(100, 100, 15)

# Add fillets to the four corners of the base plate (R10mm)
base_plate = base_plate.edges("|Z").fillet(10)

# Create the central bearing sleeve: hollow cylinder
# Outer diameter 60mm (radius 30mm), inner diameter 40mm (radius 20mm), height 40mm
# Create outer cylinder
bearing_outer = cq.Workplane("XY").circle(30).extrude(40)
# Create inner cylinder to cut out
bearing_inner = cq.Workplane("XY").circle(20).extrude(40)
# Subtract inner from outer to create hollow ring
bearing_sleeve = bearing_outer.cut(bearing_inner)

# Position the bearing sleeve starting at the top surface of base plate
# The base plate top is at z=7.5 (since it's centered at z=0, thickness 15)
# Actually, let's move base plate down so it sits at z=0 to z=15
base_plate = base_plate.translate((0, 0, 7.5))
bearing_sleeve = bearing_sleeve.translate((0, 0, 15))

# Combine base plate and bearing sleeve
part = base_plate.union(bearing_sleeve)

# Create four through-holes at the corners in an 80x80mm square pattern
# Hole diameter: 10mm (radius 5mm)
# Holes go through the entire height
hole_positions = [
    (40, 40),
    (40, -40),
    (-40, 40),
    (-40, -40)
]

for x, y in hole_positions:
    hole = cq.Workplane("XY").circle(5).extrude(55)
    hole = hole.translate((x, y, 0))
    part = part.cut(hole)

result = part
