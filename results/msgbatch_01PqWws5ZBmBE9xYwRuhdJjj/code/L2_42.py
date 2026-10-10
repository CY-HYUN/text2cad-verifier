import cadquery as cq
import math

# Create the L-shaped cross-section
# First, create an L-shaped sketch
sketch = (
    cq.Sketch()
    .rect(100, 10)  # Horizontal part of L
    .move(0, -50)
    .rect(10, 100)  # Vertical part of L
    .move(0, 50)
)

# Create the L-shape by combining rectangles
l_shape = (
    cq.Workplane("XY")
    .box(100, 10, 60, centered=True)  # Horizontal plate
    .union(
        cq.Workplane("XY")
        .box(10, 100, 60, centered=True)  # Vertical plate
    )
)

# Create the reference plane at the middle (z=0)
# The L-shape is already centered at z=0

# Find the inner corner of the L-shape (where vertical and horizontal meet)
# Inner corner is at approximately (-45, -45) in the XY plane
inner_corner_x = -45
inner_corner_y = -45

# Create a triangular rib sketch on the middle plane
# Triangle with right angle at the inner corner, with 50mm sides
rib_sketch = (
    cq.Sketch()
    .move(inner_corner_x, inner_corner_y)
    .polygon(3, 50 / math.sqrt(2))  # Create triangle
    .move(-inner_corner_x, -inner_corner_y)
)

# Create the rib by extruding the triangle with 10mm thickness
# Use a proper triangular sketch positioned at the inner corner
rib = (
    cq.Workplane("XY")
    .polyline([
        (inner_corner_x, inner_corner_y, 0),
        (inner_corner_x + 50, inner_corner_y, 0),
        (inner_corner_x, inner_corner_y + 50, 0),
        (inner_corner_x, inner_corner_y, 0)
    ])
    .close()
    .extrude(10)
)

# Union the rib with the L-shape
l_shape = l_shape.union(rib)

# Add circular holes at the center of both vertical and horizontal plates
# Hole center for horizontal plate: (0, -45, 0)
# Hole center for vertical plate: (-45, 0, 0)

hole_diameter = 20
hole_radius = hole_diameter / 2

# Create holes
l_shape = (
    l_shape
    .faces(">Z or <Z")  # Select top or bottom face
    .workplane()
    .moveTo(0, -45)
    .hole(hole_diameter)
)

l_shape = (
    l_shape
    .workplane()
    .moveTo(-45, 0)
    .hole(hole_diameter)
)

result = l_shape
