import cadquery as cq

# Base block at the left end: 20 (X) x 20 (Y) x 30 (Z), from z=0 to z=30
block = cq.Workplane("XY").box(20, 20, 30, centered=(False, True, False))

# Main strip: 100 long (X), 20 wide (Y), 10 thick (Z), sitting on top of the block (z=30..40)
strip = cq.Workplane("XY").box(100, 20, 10, centered=(False, True, False)).translate((0, 0, 30))

result = strip.union(block)
