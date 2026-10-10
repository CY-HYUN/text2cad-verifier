import cadquery as cq
import math

# Create a hemisphere by drawing a semicircle and revolving it
# Start with the front plane (XY plane, looking along Z axis)
# Draw a semicircle with radius 40mm, straight line at top

# Create semicircle profile
semicircle = (
    cq.Workplane("XY")
    .center(0, 0)
    # Draw semicircle with radius 40, center at origin
    # Arc from (40, 0) to (-40, 0) going through (0, 40)
    .moveTo(40, 0)
    .threePointArc((0, 40), (-40, 0))
    .lineTo(40, 0)  # Close with straight line at bottom, but we want it at top
)

# Actually, let's create it properly - semicircle with straight edge at top
semicircle = (
    cq.Workplane("XY")
    .moveTo(-40, 0)
    .threePointArc((0, 40), (40, 0))
    .lineTo(-40, 0)  # Straight line closes the semicircle
)

# Revolve the semicircle 180 degrees to create a hemisphere
hemisphere = semicircle.revolve(180, axis=(1, 0, 0))

# Now we need to select the top plane of the hemisphere and create two perpendicular rectangles
# The top of the hemisphere is at z=40 (the radius)

# Create a workplane on the top face of the hemisphere
top_face = hemisphere.faces(">Z").first()
sketch_plane = cq.Workplane("XY").workplane(offset=40)

# Create two concentric rectangles (10mm width) perpendicular to each other
# Both extending beyond the 40mm radius hemisphere

# First rectangle - aligned with X axis (length extends in X direction)
# Second rectangle - aligned with Y axis (length extends in Y direction)

# Create a cross-shaped sketch on the top plane
# Rectangle 1: 10mm wide in Y, extends in X direction
# Rectangle 2: 10mm wide in X, extends in Y direction

cross_sketch = (
    cq.Workplane("XY")
    .workplane(offset=40)
    .rect(100, 10)  # First rectangle: 100mm long (X), 10mm wide (Y)
)

# Add second rectangle rotated 90 degrees (10mm in X direction, 100mm in Y)
cross_sketch = cross_sketch.union(
    cq.Workplane("XY")
    .workplane(offset=40)
    .rect(10, 100)  # Second rectangle: 10mm wide (X), 100mm long (Y)
)

# Cut the cross shape downward by 20mm from the top
result = hemisphere.cut(
    cross_sketch.extrude(-20)
)
