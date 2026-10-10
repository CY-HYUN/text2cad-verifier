import cadquery as cq

# Base block 90 x 50 x 30
block = cq.Workplane("XY").rect(90.0, 50.0).extrude(30.0)

# Groove cut from top face: 90 long x 20 wide, 12 deep
result = (
    block.faces(">Z").workplane()
    .rect(90.0, 20.0)
    .cutBlind(-12.0)
)

# Fillet the two long edges at the bottom of the groove (z = 18, y = +/-10)
result = result.edges(
    cq.selectors.BoxSelector((-1.0, -11.0, 17.0), (1.0, 11.0, 19.0))
).fillet(2.0)
