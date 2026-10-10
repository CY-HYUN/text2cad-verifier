import cadquery as cq
import math

# Create a cylinder: circle with diameter 60mm, extruded 80mm
cylinder = cq.Workplane("XY").circle(30.0).extrude(80.0)

# Create the groove by revolving a rectangular profile around the Z-axis
# The rectangle represents the cross-section of the groove:
# - Radial direction: from radius 30.0 to 27.0 (depth 3.0)
# - Z direction: from 35.0 to 45.0 (width 10.0)
# Center the rectangle at radius 28.5 (midpoint between 30 and 27), Z 40 (midpoint between 35 and 45)

groove_profile = (
    cq.Workplane("XZ")
    .moveTo(28.5, 40.0)  # Position at center of groove profile
    .rect(3.0, 10.0, centered=True)  # 3mm radial depth, 10mm Z width
    .revolve(360.0)  # Revolve 360 degrees around Z-axis
)

# Cut the groove from the cylinder
result = cylinder.cut(groove_profile)

# Apply fillets with radius 1.0 to the circular edges on both sides of the groove
# Select edges parallel to Z-axis (the circular edges of the groove)
result = result.edges("|Z").fillet(1.0)
