import cadquery as cq

D = 80.0
T = 15.0
W = 10.0
depth = 5.0

disc = cq.Workplane("XY").circle(D / 2).extrude(T)

slot_x = cq.Workplane("XY").box(D + 10, W, depth, centered=(True, True, False)).translate((0, 0, T - depth))
slot_y = cq.Workplane("XY").box(W, D + 10, depth, centered=(True, True, False)).translate((0, 0, T - depth))

result = disc.cut(slot_x).cut(slot_y)
