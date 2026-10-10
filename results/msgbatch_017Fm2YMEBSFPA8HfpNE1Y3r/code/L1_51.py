import cadquery as cq
import math

# Create a disc: circle with diameter 60mm, extruded by 10mm
disc = cq.Workplane("XY").circle(30.0).extrude(10.0)

# Create a cutout circle with diameter 60mm, centered at (30.0, 0) on the top surface
# This will be extruded downward through the entire thickness (10mm)
cutout = (cq.Workplane("XY")
          .moveTo(30.0, 0)  # Position the center at (30, 0)
          .circle(30.0)  # Draw circle with diameter 60mm (radius 30mm)
          .extrude(-10.0))  # Extrude downward through the entire thickness

# Combine: subtract the cutout from the disc
result = disc.cut(cutout)
