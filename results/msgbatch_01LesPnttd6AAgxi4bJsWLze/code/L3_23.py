import cadquery as cq
import math

# Create the main rectangular block
result = cq.Workplane("XY").box(200, 100, 80)

# Add two rows of 10 vertical outlets on top (200x100 face)
# Row 1: y = 25, Row 2: y = 75
# Spacing: 200/11 = ~18.18mm, starting from x = 9.09
outlet_radius = 5
for row in [25, 75]:
    for i in range(10):
        x_pos = -100 + 10 + i * 18.18
        result = result.union(
            cq.Workplane("XY")
            .circle(outlet_radius)
            .extrude(50)
            .translate((x_pos, row, 40))
        )

# Add 3 larger oil inlets on front face (200x80), extending horizontally
inlet_radius = 10
inlet_depth = 120
for i in range(3):
    y_pos = -40 + 20 + i * 40
    x_pos = -100 + 50
    result = result.union(
        cq.Workplane("YZ")
        .circle(inlet_radius)
        .extrude(inlet_depth)
        .translate((x_pos, y_pos, 0))
    )

# Create internal main horizontal channel (inverted T connection)
# Main horizontal channel along x-axis at center height
channel_width = 20
channel_height = 15
channel_length = 150
result = result.cut(
    cq.Workplane("XY")
    .rect(channel_length, channel_width)
    .extrude(channel_height)
    .translate((0, 0, -10))
)

# Vertical connecting channels from inlets to main channel
for i in range(3):
    y_pos = -40 + 20 + i * 40
    result = result.cut(
        cq.Workplane("XZ")
        .rect(15, 30)
        .extrude(20)
        .translate((0, y_pos, 0))
    )

# Add countersunk bolt holes at corners (4 mounting holes)
bolt_radius = 3
countersink_radius = 6
countersink_depth = 5
corners = [(-90, -45, 0), (90, -45, 0), (-90, 45, 0), (90, 45, 0)]
for corner in corners:
    # Through hole
    result = result.cut(
        cq.Workplane("Z")
        .circle(bolt_radius)
        .extrude(100)
        .translate(corner)
    )
    # Countersink
    result = result.cut(
        cq.Workplane("Z")
        .circle(countersink_radius)
        .extrude(countersink_depth)
        .translate((corner[0], corner[1], 40))
    )

# Add 4 weight-reduction oval grooves on bottom/side surfaces
groove_length = 40
groove_width = 15
groove_depth = 8

# Bottom groove 1 (center left)
result = result.cut(
    cq.Workplane("XY")
    .rect(groove_length, groove_width)
    .extrude(groove_depth)
    .translate((-50, 0, -40))
)

# Bottom groove 2 (center right)
result = result.cut(
    cq.Workplane("XY")
    .rect(groove_length, groove_width)
    .extrude(groove_depth)
    .translate((50, 0, -40))
)

# Side groove 1 (left side)
result = result.cut(
    cq.Workplane("YZ")
    .rect(groove_length, groove_width)
    .extrude(groove_depth)
    .translate((-100, 0, -15))
)

# Side groove 2 (right side)
result = result.cut(
    cq.Workplane("YZ")
    .rect(groove_length, groove_width)
    .extrude(groove_depth)
    .translate((100, 0, -15))
)
