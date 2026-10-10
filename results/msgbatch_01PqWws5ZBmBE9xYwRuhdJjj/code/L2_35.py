import cadquery as cq
import math

# Start with a 60mm cube
cube = cq.Workplane("XY").box(60, 60, 60)

# First hole: Right view plane (YZ plane), circle at Z=5mm, cut along X-axis
# Right view means we're looking at the YZ plane
# Create a circle in the YZ plane at Z=5mm with 20mm diameter (10mm radius)
hole1 = (cq.Workplane("YZ")
         .center(0, 5)  # Move to Z=5mm (vertical in YZ plane)
         .circle(10)    # 20mm diameter = 10mm radius
         .extrude(100, both=True))  # Cut completely through along X-axis

# Second hole: Front view plane (XZ plane), circle at Z=-5mm, cut along Y-axis
# Front view means we're looking at the XZ plane
# Create a circle in the XZ plane at Z=-5mm with 20mm diameter (10mm radius)
hole2 = (cq.Workplane("XZ")
         .center(0, -5)  # Move to Z=-5mm (vertical in XZ plane)
         .circle(10)     # 20mm diameter = 10mm radius
         .extrude(100, both=True))  # Cut completely through along Y-axis

# Cut both holes from the cube
result = cube.cut(hole1).cut(hole2)
