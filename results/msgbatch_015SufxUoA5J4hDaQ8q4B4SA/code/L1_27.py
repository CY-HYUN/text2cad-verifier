import cadquery as cq

# Horizontal strip sits on top of the block (z from 30 to 40)
strip = cq.Workplane("XY").box(100, 20, 10, centered=False).translate((0, 0, 30))
# Base block at the left end (z from 0 to 30)
block = cq.Workplane("XY").box(20, 20, 30, centered=False)
result = strip.union(block)
