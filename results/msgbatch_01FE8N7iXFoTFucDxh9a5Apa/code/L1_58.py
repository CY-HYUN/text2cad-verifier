import cadquery as cq

# Main body: 90 x 50 x 30 block, bottom face centred on the origin
body = cq.Workplane("XY").box(90, 50, 30, centered=(True, True, False))

# Through slot along X: 20 mm wide, 12 mm deep from the top face (z = 18 to 30)
slot = (
    cq.Workplane("XY")
    .workplane(offset=30 - 12)
    .box(90, 20, 12 + 1, centered=(True, True, False))
)
result = body.cut(slot)

# Fillet the two long edges where the slot floor meets the side walls
result = result.edges(
    cq.selectors.BoxSelector((-50, -11, 17), (50, 11, 19))
).fillet(2)
