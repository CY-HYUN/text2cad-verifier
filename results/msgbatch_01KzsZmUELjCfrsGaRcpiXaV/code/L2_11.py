import cadquery as cq
import math

# Create base rectangular prism
base = cq.Workplane("XY").box(60, 40, 40)

# Create two holes on the top surface
# Holes are 10mm diameter, spaced 30mm apart
# Position them at y=0 (center), x = ±15mm from center
hole_diameter = 10
hole_radius = hole_diameter / 2
spacing = 30

# Hole positions relative to center of top surface
hole_x_positions = [-spacing/2, spacing/2]  # -15, 15

# Create two cylindrical holes from top
for x_pos in hole_x_positions:
    base = base.faces(">Z").workplane().moveTo(x_pos, 0).hole(hole_diameter)

# Create internal channel by subtracting from the main body
# Channel positioned 5mm below the top surface
# Channel runs from x=-15 to x=15, width 10mm, height 10mm
channel_length = 30  # spans the 30mm distance between holes
channel_width = 10  # same diameter as holes

# Create the internal U-shaped channel as a box
# Position it in 3D space using a new workplane
channel_box = cq.Workplane("XY").box(channel_length, channel_width, channel_width, centered=True)

# Move the channel to the correct position (5mm below top surface)
# The top surface is at z=20, so channel top should be at z=15
channel_box = channel_box.translate((0, 0, -5))

# Subtract the channel from the base
result = base.cut(channel_box)
