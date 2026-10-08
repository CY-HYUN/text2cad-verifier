import cadquery as cq

# Base block 90 x 50 x 30, centered in XY, sitting on z=0
block = cq.Workplane("XY").rect(90.0, 50.0).extrude(30.0)

# Groove: 90 long (full length along X), 20 wide, 12 deep from top face
grooved = (
    block.faces(">Z").workplane()
    .rect(90.0, 20.0)
    .cutBlind(-12.0)
)

# Fillet the two long edges at the bottom of the groove (z = 18, y = +/-10)
result = (
    grooved.edges("|X")
    .edges(cq.selectors.BoxSelector((-50.0, -11.0, 17.0), (50.0, 11.0, 19.0)))
    .fillet(2.0)
)
