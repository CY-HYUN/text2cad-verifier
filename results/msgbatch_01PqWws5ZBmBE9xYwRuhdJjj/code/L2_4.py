import cadquery as cq
import math

# Create the base plate: 100x100mm rectangle, extruded 15mm
base_plate = cq.Workplane("XY").rect(100, 100).extrude(15)

# Select the top surface of the base plate and create the bearing seat
# Draw a concentric circle (annulus) with outer diameter 60mm and inner diameter 40mm
# Extrude 40mm upward
bearing_seat = (
    base_plate
    .faces(">Z")
    .workplane()
    .circle(30)  # outer radius 30mm (diameter 60mm)
    .circle(20)  # inner radius 20mm (diameter 40mm)
    .extrude(40)
)

# Select the top surface of the base plate to add mounting holes
# Four circles with diameter 10mm at vertices of 80mm square centered at origin
# Vertices at (±40, ±40)
mounting_holes = (
    bearing_seat
    .faces(">Z")
    .workplane(origin=(0, 0, 15))  # workplane at top of base plate
    .pushPoints([
        (40, 40),
        (40, -40),
        (-40, 40),
        (-40, -40)
    ])
    .circle(5)  # radius 5mm (diameter 10mm)
    .cutThruAll()
)

# Apply fillet to the four vertical edges of the base plate
# Select edges at the top perimeter of the base plate (where it meets z=15)
result = mounting_holes.edges("|Z").fillet(10)
