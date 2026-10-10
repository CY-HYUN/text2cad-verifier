import cadquery as cq

L, W, H = 90.0, 50.0, 30.0
slot_w, slot_d = 20.0, 12.0
r = 2.0

body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

cutter = (
    cq.Workplane("XY")
    .box(L + 2, slot_w, slot_d + 1, centered=(True, True, False))
    .translate((0, 0, H - slot_d))
)

result = body.cut(cutter)

z_bot = H - slot_d
result = result.edges(
    cq.selectors.BoxSelector((-L, -slot_w / 2 - 0.5, z_bot - 0.5),
                             (L, slot_w / 2 + 0.5, z_bot + 0.5))
).fillet(r)
