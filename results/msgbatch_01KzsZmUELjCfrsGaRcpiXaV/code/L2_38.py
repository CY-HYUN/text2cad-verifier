import cadquery as cq
import math

# Create the horizontal cylindrical pipe (X-axis) with diameter 50mm, length 120mm
horizontal_pipe = cq.Workplane("XY").cylinder(height=120, radius=25, centered=True)

# Create the vertical cylindrical pipe (Z-axis) with diameter 50mm, length 80mm
# Position it so it extends from z=0 to z=80
vertical_pipe = cq.Workplane("XY").cylinder(height=80, radius=25, centered=False)

# Union the two pipes
combined = horizontal_pipe.union(vertical_pipe)

# Create the through-hole along X-axis (40mm diameter = 20mm radius)
# Make it long enough to go through the entire part
hole_x = cq.Workplane("YZ").cylinder(height=150, radius=20, centered=True)

# Create the through-hole along Z-axis (40mm diameter = 20mm radius)
# Make it long enough to go through the entire part
hole_z = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)

# Subtract both holes from the combined pipes
result = combined.cut(hole_x).cut(hole_z)
