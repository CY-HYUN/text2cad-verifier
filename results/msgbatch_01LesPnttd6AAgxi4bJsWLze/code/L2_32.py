import cadquery as cq
import math

# Create a plum blossom column by arranging 6 cylinders around a circle
# Each cylinder has diameter 20mm, arranged on a circle with diameter 20mm (radius 10mm)
# The cylinders will overlap significantly, creating a petal-like appearance

# Parameters
cylinder_diameter = 20
cylinder_radius = cylinder_diameter / 2
array_circle_radius = 10  # Circle diameter is 20mm, so radius is 10mm
num_cylinders = 6
cylinder_height = 30  # Height of each cylinder

# Start with an empty workplane
result = None

# Create 6 cylinders arranged around the circle
for i in range(num_cylinders):
    # Calculate angle for this cylinder
    angle = (i * 360) / num_cylinders
    angle_rad = math.radians(angle)
    
    # Calculate position on the circle
    x = array_circle_radius * math.cos(angle_rad)
    y = array_circle_radius * math.sin(angle_rad)
    
    # Create a cylinder at this position
    # Use a workplane at the calculated position
    cylinder = cq.Workplane("XY").center(x, y).cylinder(
        height=cylinder_height,
        radius=cylinder_radius,
        centered=True
    )
    
    # Union the cylinder with the result
    if result is None:
        result = cylinder
    else:
        result = result.union(cylinder)

# Ensure result is not None (should never happen with 6 cylinders, but be safe)
if result is None:
    result = cq.Workplane("XY").cylinder(height=cylinder_height, radius=cylinder_radius, centered=True)
