import cadquery as cq
import math

# Create a new part with units in millimeters
# Start with a cylinder: diameter 50mm, height 80mm
cylinder = cq.Workplane("XY").circle(25).extrude(80)

# Create the annular groove
# The groove is on the XZ plane, revolved around Z-axis
# Outer radius of cylinder: 25mm
# Groove depth (radial): 5mm, so inner radius: 25 - 5 = 20mm
# Groove width (axial): 10mm, centered at z=40mm, so from z=35 to z=45

# Create a 2D profile on the XZ plane for the groove
# The profile should be a rectangle that, when revolved, creates the groove
# We need to sketch from the XZ plane perspective

# Create the groove profile on XZ plane
groove_sketch = (
    cq.Workplane("XZ")
    .rect(5, 10)  # 5mm radial depth, 10mm axial width
    .translate((20, 40, 0))  # Position at radius 20 (inner edge), centered at z=40
)

# Revolve the groove profile 360 degrees around the Z-axis
groove = groove_sketch.revolve(360, (0, 0, 0), (0, 0, 1))

# Cut the groove from the cylinder
result = cylinder.cut(groove)
