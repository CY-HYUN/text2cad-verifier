import cadquery as cq
import math

# Create the U-shaped cross-section sketch on the front plane
sketch = (
    cq.Sketch()
    .rect(80, 10, mode="center")  # Bottom: 80mm wide, 10mm high
    .moveTo(-40, 5)  # Move to left side bottom
    .rect(10, 40, mode="center")  # Left flange: 10mm wide, 40mm high
    .moveTo(40, 5)  # Move to right side bottom
    .rect(10, 40, mode="center")  # Right flange: 10mm wide, 40mm high
)

# Create the base solid by extruding the sketch 40mm
result = (
    cq.Workplane("front")
    .placeSketch(sketch)
    .extrude(40)
)

# Select the outer side of the left flange and cut a 10mm diameter hole through
result = (
    result
    .faces("|X")  # Select faces perpendicular to X axis
    .workplane()
    .center(-40, 20)  # Position at left flange outer surface, top area
    .hole(10, 40)  # 10mm diameter hole through (depth > part thickness)
)

# Select the outer side of the right flange
# First, cut a 10mm diameter hole through
result = (
    result
    .faces("|X")
    .workplane()
    .center(40, 20)  # Position at right flange outer surface, top area
    .hole(10, 40)  # 10mm diameter hole through
)

# Then cut a 20mm diameter countersunk hole to 2mm depth on the right flange
result = (
    result
    .faces("|X")
    .workplane()
    .center(40, 20)
    .hole(20, 2)  # 20mm diameter hole, 2mm deep
)
