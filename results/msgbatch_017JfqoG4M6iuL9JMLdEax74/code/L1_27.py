import cadquery as cq

# Main strip: 100 long (X), 20 wide (Y), 10 thick (Z), sitting on top
strip = cq.Workplane("XY").box(100, 20, 10, centered=(False, True, False)).translate((0, 0, 20))

# Base block at the left end: 20 x 20 x 30, from z=0 to z=30
block = cq.Workplane("XY").box(20, 20, 30, centered=(False, True, False))

result = strip.union(block)
