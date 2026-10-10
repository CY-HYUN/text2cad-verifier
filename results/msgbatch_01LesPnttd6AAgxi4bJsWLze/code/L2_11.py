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

# Now create the internal U-shaped channel connecting the two holes
# The channel runs horizontally beneath the top surface
# Channel dimensions: 10mm diameter (same as holes)
channel_radius = 5  # 10mm diameter channel

# Create a U-shaped path for the internal channel
# Start from left hole, go horizontally to right hole
# The channel should be at a depth below the top surface

# Create the U-shaped channel by subtracting a swept shape
# We'll create this by making a horizontal rectangular channel
channel_depth = 10  # channel goes down 10mm from top
channel_length = 30  # spans the 30mm distance between holes
channel_width = 10  # same diameter as holes

# Create channel as a rectangular prism positioned internally
# The channel connects the two hole positions horizontally
channel = (cq.Workplane("XY")
    .moveTo(-spacing/2, 0)
    .rect(channel_length, channel_width)
    .extrude(channel_depth, taper=0)
)

# We need to position and orient this channel properly
# Create a horizontal channel from left hole to right hole
# Using a different approach: create using box and position it

# Create internal channel by subtracting from the main body
# Channel positioned 5mm below the top surface (depth 40-5=35 to top)
# Channel runs from x=-15 to x=15, width 10mm, height 10mm

channel_box = (cq.Workplane("XY")
    .moveTo(0, 0, 35)  # positioned 5mm below top surface
    .box(channel_length, channel_width, channel_width, centered=True)
)

# Subtract the channel from the base
result = base.cut(channel_box)
