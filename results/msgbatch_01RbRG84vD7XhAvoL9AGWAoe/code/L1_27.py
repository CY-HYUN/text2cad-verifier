import cadquery as cq

# Main strip: 100 (X) x 20 (Y) x 10 (Z), sitting from z=0 to z=10
strip = cq.Workplane("XY").box(100, 20, 10, centered=(False, True, False))

# Base block at the left end, below the strip: 20 x 20 x 30, from z=-30 to z=0
block = (
    cq.Workplane("XY")
    .box(20, 20, 30, centered=(False, True, False))
    .translate((0, 0, -30))
)

result = strip.union(block)
