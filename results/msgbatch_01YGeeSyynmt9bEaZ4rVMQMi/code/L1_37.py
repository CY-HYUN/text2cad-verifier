import cadquery as cq

D = 80.0
H = 15.0
slot_w = 10.0
slot_len = 100.0
cut_depth = 5.0

disk = cq.Workplane("XY").circle(D / 2).extrude(H)

slot1 = (
    cq.Workplane("XY")
    .workplane(offset=H - cut_depth)
    .rect(slot_len, slot_w)
    .extrude(cut_depth + 1)
)
slot2 = (
    cq.Workplane("XY")
    .workplane(offset=H - cut_depth)
    .rect(slot_w, slot_len)
    .extrude(cut_depth + 1)
)

result = disk.cut(slot1).cut(slot2)
