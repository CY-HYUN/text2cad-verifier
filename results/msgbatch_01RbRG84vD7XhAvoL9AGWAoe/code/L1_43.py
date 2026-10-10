import cadquery as cq

L, W, H = 100.0, 50.0, 30.0
gw, gh = 30.0, 20.0

body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))
groove = cq.Workplane("XY").box(L + 2, gw, gh + 1, centered=(True, True, False)).translate((0, 0, H - gh))
result = body.cut(groove)
