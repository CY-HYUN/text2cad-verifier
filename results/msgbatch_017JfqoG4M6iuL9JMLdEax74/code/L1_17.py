import cadquery as cq

L, H, T = 60.0, 30.0, 20.0
R = 20.0

block = cq.Workplane("XY").box(L, H, T, centered=(True, False, False))
cyl = cq.Workplane("XY").circle(R).extrude(T)
result = block.cut(cyl)
