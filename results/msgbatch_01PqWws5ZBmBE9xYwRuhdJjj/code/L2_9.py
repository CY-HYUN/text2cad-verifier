import cadquery as cq
import math

# Create base ring by extruding two concentric circles
base = cq.Workplane("XY").circle(40).circle(25).extrude(10)

# Get the top face of the ring for the tooth sketch
top_face = base.faces(">Z").first()

# Create tooth sketch on the top face
# A single ratchet tooth: triangular shape extending radially outward
tooth_sketch = (
    cq.Workplane("XY")
    .moveTo(40, 0)  # Start at outer circumference
    .lineTo(45, 0)  # Extend 5mm radially outward
    .lineTo(40, 2)  # Slanted line back to circumference
    .close()  # Close the triangle
)

# Extrude the tooth sketch
tooth = tooth_sketch.extrude(10)

# Combine base ring with one tooth
combined = base.union(tooth)

# Create a circular array of the tooth feature
# We need to create 12 teeth distributed evenly around the circumference
# Each tooth is rotated by 360/12 = 30 degrees

result = base
for i in range(1, 12):
    angle = i * 30  # 30 degrees per tooth
    # Create tooth at rotated position
    tooth_rotated = (
        cq.Workplane("XY")
        .moveTo(40 * math.cos(math.radians(angle)), 40 * math.sin(math.radians(angle)))
        .lineTo(45 * math.cos(math.radians(angle)), 45 * math.sin(math.radians(angle)))
        .lineTo((40 * math.cos(math.radians(angle)) + 2 * math.cos(math.radians(angle + 90))), 
                (40 * math.sin(math.radians(angle)) + 2 * math.sin(math.radians(angle + 90))))
        .close()
        .extrude(10)
    )
    result = result.union(tooth_rotated)
