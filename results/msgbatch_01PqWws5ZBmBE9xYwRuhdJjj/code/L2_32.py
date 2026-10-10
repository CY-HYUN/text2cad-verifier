import cadquery as cq
import math

# Create a single cylinder with diameter 20 mm and height 10 mm
cylinder = cq.Workplane("XY").cylinder(height=10, radius=10)

# Create a pattern by placing 6 cylinders in a circular array
# The cylinders are offset 10 mm from the origin (where the circle diameter is 20mm, radius 10mm)
result = cq.Workplane("XY")

# Create 6 copies arranged in a circular pattern
for i in range(6):
    angle = (i * 360 / 6) * math.pi / 180
    x_offset = 10 * math.cos(angle)
    y_offset = 10 * math.sin(angle)
    
    # Create a single cylinder at the offset position
    single_cyl = cq.Workplane("XY").cylinder(height=10, radius=10).translate((x_offset, y_offset, 0))
    
    if i == 0:
        result = single_cyl
    else:
        result = result.union(single_cyl)

