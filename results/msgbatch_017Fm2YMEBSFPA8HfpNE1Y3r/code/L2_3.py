import cadquery as cq
import math

# Create a hemisphere by drawing a semicircle and revolving it
# Start with a semicircle profile on the XZ plane

# Create semicircle profile (in XZ plane, will revolve around Z axis)
semicircle = (
    cq.Workplane("XZ")
    .moveTo(-40, 0)
    .threePointArc((0, 40), (40, 0))
    .lineTo(-40, 0)  # Straight line closes the semicircle
)

# Revolve the semicircle 180 degrees around the Y axis to create a hemisphere
hemisphere = semicircle.revolve(180)

# Now create two perpendicular rectangles on the top plane
# The rectangles are 10mm wide and extend beyond the hemisphere edge

# Create a workplane on the top of the hemisphere (at z=40)
top_sketch = (
    cq.Workplane("XY")
    .workplane(offset=40)
    .rect(100, 10)  # First rectangle: 100mm in X, 10mm in Y
)

# Add the second rectangle perpendicular to the first
# Create it separately and union, or use a combined approach
top_sketch = top_sketch.union(
    cq.Workplane("XY")
    .workplane(offset=40)
    .rect(10, 100)  # Second rectangle: 10mm in X, 100mm in Y
)

# Extrude the cross-shaped sketch downward by 20mm to cut into the hemisphere
cut_tool = top_sketch.extrude(-20)

# Perform the cut operation
result = hemisphere.cut(cut_tool)
