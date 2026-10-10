import cadquery as cq
import math

# Create a cylinder: circle with diameter 60mm, extruded 80mm
workplane = cq.Workplane("XY")
cylinder = workplane.circle(30.0).extrude(80.0)

# Switch to XZ plane for the groove sketch
# The groove is defined as:
# - Radial depth: from 30.0 to 27.0 (3mm depth)
# - Z height: from 35.0 to 45.0 (10mm width)
groove_sketch = (
    cq.Workplane("XZ")
    .rect(3.0, 10.0)  # width 3mm (radial), height 10mm (Z direction)
    .located(cq.Location(cq.Vector(28.5, 0, 40.0)))  # centered at radius 28.5, Z 40
)

# Create a revolved cut (360 degrees around Z-axis)
# First, create the base cylinder and cut with revolved sketch
result = cylinder.cut(
    cq.Workplane("XZ")
    .moveTo(28.5, 40.0)  # move to center of groove (radial 28.5, Z 40)
    .rect(3.0, 10.0, centered=True)
    .revolve(360, axisEnd=cq.Vector(0, 0, 1))
)

# Apply fillets with radius 1.0 to circular edges on both sides of the groove
# Find edges that are circular and near the groove location
result = result.edges("|Z").fillet(1.0)

