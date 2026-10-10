import cadquery as cq

# Create the main strip body (100mm long, 20mm wide, 10mm thick)
# X-axis is length (100mm), Y-axis is width (20mm), Z-axis is thickness (10mm)
main_strip = cq.Workplane("XY").box(100, 20, 10)

# Create the base block (20mm long, 20mm wide, 30mm high)
# X-axis is length (20mm), Y-axis is width (20mm), Z-axis is height (30mm)
# Position at the lower left end of the strip
# The strip is 100mm long in X, so left end is at X = -50
# The base block should be centered at the left end

# Strip goes from X = -50 to X = 50, Y = -10 to Y = 10, Z = -5 to Z = 5
# Base block: X from -60 to -40 (20mm long), Y from -10 to 10 (20mm wide), Z from -35 to -5 (30mm high)
base_block = cq.Workplane("XY").box(20, 20, 30).translate((-60, 0, -17.5))

# Combine both parts into a single unit
result = main_strip.union(base_block)
