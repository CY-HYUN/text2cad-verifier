import cadquery as cq

L, W, H = 100.0, 50.0, 30.0
slot_w, slot_d = 20.0, 15.0

body = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))
slot = cq.Workplane("XY").box(L + 2, slot_w, slot_d + 1).translate((0, 0, H - slot_d + (slot_d + 1) / 2))
result = body.cut(slot)
