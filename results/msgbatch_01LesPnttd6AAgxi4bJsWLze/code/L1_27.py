import cadquery as cq

# Create the main strip body (100mm long, 20mm wide, 10mm thick)
# Positioned along X-axis, centered on Y-axis
main_strip = cq.Workplane("XY").box(100, 20, 10)

# Create the base block (20mm long, 20mm wide, 30mm high)
# Positioned at the lower left end (negative X direction)
# The base should be at the "lower" end, so it extends downward in Z
# and is positioned at the negative X end of the strip

# First, let's position the main strip so its center is at origin
# The strip goes from X = -50 to X = 50, Y = -10 to Y = 10, Z = -5 to Z = 5

# The base block should be:
# - At the left end: X from -50 to -30 (20mm long in X direction)
# - Full width: Y from -10 to 10 (20mm wide in Y direction)
# - Below: Z from -35 to -5 (30mm high, attached to bottom of strip at Z=-5)

base_block = cq.Workplane("XY").box(20, 20, 30).translate((-40, 0, -17.5))

# Combine both parts into a single unit
result = main_strip.union(base_block)
