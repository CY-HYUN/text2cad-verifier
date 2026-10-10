import cadquery as cq

# Main block: 90 x 50 x 30, bottom center at origin
block = cq.Workplane("XY").box(90, 50, 30, centered=(True, True, False))

# Through slot: 20 wide (Y), full length in X, 12 deep from top (z=30 down to z=18)
slot = cq.Workplane("XY").workplane(offset=18).rect(90, 20).extrude(12)
body = block.cut(slot)

# Fillet the two long edges at the slot bottom (z=18, along X, at y=±10)
result = body.edges(cq.selectors.BoxSelector((-50, -11, 17), (50, 11, 19))).edges("|X").fillet(2)
