import cadquery as cq

# Main block: 90 x 50 x 30, origin at center of bottom face
block = cq.Workplane("XY").box(90, 50, 30, centered=(True, True, False))

# Through slot along X on top surface: width 20 (Y), depth 12
slot = (
    cq.Workplane("XY")
    .workplane(offset=30 - 12)
    .rect(90, 20)
    .extrude(12)
)

body = block.cut(slot)

# Fillet the two long edges where slot bottom meets side walls (R2)
body = body.edges(
    cq.selectors.BoxSelector((-50, -11, 17), (50, 11, 19))
).edges("|X").fillet(2)

result = body
