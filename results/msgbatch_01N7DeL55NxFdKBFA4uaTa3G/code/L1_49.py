import cadquery as cq

L = 40.0
d = 10.0

cube = cq.Workplane("XY").box(L, L, L)

hz = cq.Workplane("XY").circle(d / 2).extrude(L * 2, both=True)
hx = cq.Workplane("YZ").circle(d / 2).extrude(L * 2, both=True)
hy = cq.Workplane("XZ").circle(d / 2).extrude(L * 2, both=True)

result = cube.cut(hz).cut(hx).cut(hy)
