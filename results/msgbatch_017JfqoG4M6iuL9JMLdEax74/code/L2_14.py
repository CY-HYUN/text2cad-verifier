import cadquery as cq

L = 60.0
H = 40.0

cube = cq.Workplane("XY").box(L, L, L)
cx = cq.Workplane("XY").box(L * 2, H, H)
cy = cq.Workplane("XY").box(H, L * 2, H)
cz = cq.Workplane("XY").box(H, H, L * 2)

result = cube.cut(cx).cut(cy).cut(cz)
