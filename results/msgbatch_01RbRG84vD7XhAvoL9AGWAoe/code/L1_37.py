import cadquery as cq

D = 80.0
T = 15.0
slot_w = 10.0
slot_d = 5.0

# Main disc, bottom at z=0, top at z=T
disc = cq.Workplane("XY").circle(D / 2).extrude(T)

# Cross slots cut from the top surface, running edge to edge
L = D + 10.0
slot_x = (
    cq.Workplane("XY")
    .box(L, slot_w, slot_d, centered=(True, True, False))
    .translate((0, 0, T - slot_d))
)
slot_y = (
    cq.Workplane("XY")
    .box(slot_w, L, slot_d, centered=(True, True, False))
    .translate((0, 0, T - slot_d))
)

result = disc.cut(slot_x).cut(slot_y)
