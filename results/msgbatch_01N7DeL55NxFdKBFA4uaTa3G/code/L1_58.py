import cadquery as cq

# Base block 90 x 50 x 30
block = cq.Workplane("XY").rect(90.0, 50.0).extrude(30.0)

# Groove: 90 long (X), 20 wide (Y), 12 deep from top face
groove = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - 12.0)
    .rect(90.0, 20.0)
    .extrude(12.0)
)
body = block.cut(groove)

# Fillet the two long bottom edges of the groove (z = 18, y = +/-10)
result = body.edges(
    cq.selectors.BoxSelector((-50.0, -11.0, 17.0), (50.0, 11.0, 19.0))
).fillet(2.0)
