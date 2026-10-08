import cadquery as cq

L, W, H = 90.0, 50.0, 30.0
slot_w, slot_d = 20.0, 12.0
r = 2.0

# Main block with bottom face centered at origin
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Through slot along X in the top surface
slot = (
    cq.Workplane("XY")
    .box(L + 2, slot_w, slot_d + 1, centered=(True, True, False))
    .translate((0, 0, H - slot_d))
)
body = body.cut(slot)

# Fillet the two long edges where slot bottom meets side walls
zb = H - slot_d
result = body.edges(
    cq.selectors.BoxSelector(
        (-L, -slot_w / 2 - 0.1, zb - 0.1),
        (L, slot_w / 2 + 0.1, zb + 0.1),
    )
).edges("|X").fillet(r)
