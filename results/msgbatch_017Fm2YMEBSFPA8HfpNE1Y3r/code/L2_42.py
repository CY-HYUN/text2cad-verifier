import cadquery as cq
import math

# Create the L-shaped cross-section by combining two boxes
l_shape = (
    cq.Workplane("XY")
    .box(100, 10, 60, centered=True)  # Horizontal plate
    .union(
        cq.Workplane("XY")
        .box(10, 100, 60, centered=True)  # Vertical plate
    )
)

# Inner corner of the L-shape
inner_corner_x = -45
inner_corner_y = -45

# Create the triangular rib at the middle plane
# Triangle with right angle at inner corner, with 50mm legs
rib = (
    cq.Workplane("XY")
    .polyline([
        (inner_corner_x, inner_corner_y),
        (inner_corner_x + 50, inner_corner_y),
        (inner_corner_x, inner_corner_y + 50)
    ])
    .close()
    .extrude(10)
)

# Union the rib with the L-shape
l_shape = l_shape.union(rib)

# Add circular holes through both vertical and horizontal plates
# Hole at center of horizontal plate
l_shape = (
    l_shape
    .workplane()
    .moveTo(0, -45)
    .hole(20)
)

# Hole at center of vertical plate
l_shape = (
    l_shape
    .workplane()
    .moveTo(-45, 0)
    .hole(20)
)

result = l_shape
