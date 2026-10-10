import cadquery as cq
import math

# Create the horizontal cylindrical pipe (X-axis)
horizontal_pipe = cq.Workplane("XY").cylinder(height=120, radius=25, centered=True)

# Create the vertical cylindrical pipe (Z-axis)
vertical_pipe = cq.Workplane("XY").cylinder(height=80, radius=25, centered=False).rotate((1, 0, 0), (0, 0, 0), 90)

# Union the two pipes
combined = horizontal_pipe.union(vertical_pipe)

# Create the through-hole along X-axis (40mm diameter = 20mm radius)
hole_x = cq.Workplane("YZ").cylinder(height=150, radius=20, centered=True)

# Create the through-hole along Z-axis (40mm diameter = 20mm radius)
hole_z = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)

# Subtract both holes from the combined pipes
result = combined.cut(hole_x).cut(hole_z)
