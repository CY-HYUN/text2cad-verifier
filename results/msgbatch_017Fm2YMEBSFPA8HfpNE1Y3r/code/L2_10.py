import cadquery as cq
import math

# Create the base solid by extruding the U-shaped cross-section
# Bottom rectangle: 80mm wide, 10mm high
# Left flange: 10mm wide, 40mm high, positioned at left
# Right flange: 10mm wide, 40mm high, positioned at right

result = (
    cq.Workplane("front")
    .moveTo(-40, 5)
    .lineTo(-45, 5)
    .lineTo(-45, 45)
    .lineTo(-35, 45)
    .lineTo(-35, 15)
    .lineTo(35, 15)
    .lineTo(35, 45)
    .lineTo(45, 45)
    .lineTo(45, 5)
    .lineTo(40, 5)
    .lineTo(40, 0)
    .lineTo(-40, 0)
    .close()
    .extrude(40)
)

# Select the outer side of the left flange and cut a 10mm diameter hole through
result = (
    result
    .faces("<X")  # Select left face (negative X direction)
    .workplane()
    .center(-5, 25)  # Position at left flange, centered vertically on the 40mm height
    .hole(10, 40)  # 10mm diameter hole through
)

# Select the outer side of the right flange and cut a 10mm diameter hole through
result = (
    result
    .faces(">X")  # Select right face (positive X direction)
    .workplane()
    .center(5, 25)  # Position at right flange, centered vertically
    .hole(10, 40)  # 10mm diameter hole through
)

# Cut a 20mm diameter countersunk hole to 2mm depth on the right flange
result = (
    result
    .faces(">X")
    .workplane()
    .center(5, 25)
    .hole(20, 2)  # 20mm diameter hole, 2mm deep (pocket)
)
