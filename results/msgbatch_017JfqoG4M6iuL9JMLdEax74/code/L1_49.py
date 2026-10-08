import cadquery as cq

L = 40.0
d = 10.0

cube = cq.Workplane("XY").box(L, L, L)
cz = cq.Workplane("XY").cylinder(L * 1.5, d / 2)
cx = cq.Workplane("YZ").cylinder(L * 1.5, d / 2)
cy = cq.Workplane("XZ").cylinder(L * 1.5, d / 2)

result = cube.cut(cz).cut(cx).cut(cy)
