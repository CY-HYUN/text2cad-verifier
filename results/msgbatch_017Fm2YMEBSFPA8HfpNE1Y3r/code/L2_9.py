import cadquery as cq
import math

# Create base ring by extruding two concentric circles
base = cq.Workplane("XY").circle(40).circle(25).extrude(10)

# Create tooth sketch on the XY plane before union
# A single ratchet tooth: triangular shape extending radially outward
tooth_sketch = (
    cq.Workplane("XY")
    .moveTo(40, 0)  # Start at outer circumference
    .lineTo(45, 0)  # Extend 5mm radially outward
    .lineTo(40, 2)  # Slanted line back to circumference
    .close()  # Close the triangle
)

# Extrude the tooth sketch 10mm
tooth = tooth_sketch.extrude(10)

# Start with base ring
result = base.union(tooth)

# Create 11 more teeth distributed evenly around the circumference (12 total)
# Each tooth is rotated by 360/12 = 30 degrees
for i in range(1, 12):
    angle = i * 30  # 30 degrees per tooth
    cos_a = math.cos(math.radians(angle))
    sin_a = math.sin(math.radians(angle))
    cos_a90 = math.cos(math.radians(angle + 90))
    sin_a90 = math.sin(math.radians(angle + 90))
    
    # Create tooth at rotated position
    tooth_rotated = (
        cq.Workplane("XY")
        .moveTo(40 * cos_a, 40 * sin_a)
        .lineTo(45 * cos_a, 45 * sin_a)
        .lineTo(40 * cos_a + 2 * cos_a90, 40 * sin_a + 2 * sin_a90)
        .close()
        .extrude(10)
    )
    result = result.union(tooth_rotated)
