import cadquery as cq
import math

# Create the base disc
disc = cq.Workplane("XY").circle(40).extrude(10)

# Create the radial slots (4 U-shaped slots evenly distributed)
# Each slot is 8mm wide, 25mm long, with semicircular bottom
slot_width = 8
slot_length = 25
slot_depth = 25  # depth pointing toward center

# Create a single slot profile (U-shaped)
# The slot will be created as a rectangle with a semicircular bottom
slot_profile = (
    cq.Workplane("XY")
    .moveTo(-slot_width/2, 0)
    .lineTo(-slot_width/2, -slot_length + slot_width/2)
    .radiusArc((-slot_width/2 + slot_width, -slot_length + slot_width/2), slot_width/2)
    .lineTo(slot_width/2, 0)
    .close()
)

# Create 4 slots at 90-degree intervals
result = disc
for i in range(4):
    angle = i * 90
    # Position each slot at the edge of the disc, pointing outward
    slot_pad = (
        cq.Workplane("XY")
        .rect(slot_width, slot_length, forConstruction=False)
        .extrude(10)
    )
    # Move slot to edge and rotate
    slot_pad = slot_pad.translate((40 - slot_length/2, 0, 0))
    slot_pad = slot_pad.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(slot_pad)

# Create semicircular cutouts on the circumference between slots
cutout_radius = 20
for i in range(4):
    angle = i * 90 + 45  # Between the slots
    rad = math.radians(angle)
    # Position at the edge
    x = 40 * math.cos(rad)
    y = 40 * math.sin(rad)
    
    # Create semicircular cutout
    cutout = (
        cq.Workplane("XY")
        .moveTo(x, y)
        .circle(cutout_radius)
        .extrude(-10)
    )
    result = result.cut(cutout)

# Create the central shaft hole
shaft_hole = cq.Workplane("XY").circle(5).extrude(-10)
result = result.cut(shaft_hole)

result = result.translate((0, 0, 5))
