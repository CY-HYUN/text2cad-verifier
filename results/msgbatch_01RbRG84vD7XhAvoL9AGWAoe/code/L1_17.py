import cadquery as cq

L, H, T, R = 60.0, 30.0, 20.0, 20.0

body = cq.Workplane("XY").box(L, H, T, centered=(True, False, False))
cyl = cq.Workplane("XY").circle(R).extrude(T)
result = body.cut(cyl)
