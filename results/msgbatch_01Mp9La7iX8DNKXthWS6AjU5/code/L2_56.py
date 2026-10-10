import cadquery as cq

L = 100
R = 20
t = 2

# outer cross
cx = cq.Workplane("YZ").circle(R).extrude(L / 2, both=True)
cy = cq.Workplane("XZ").circle(R).extrude(L / 2, both=True)
outer = cx.union(cy)

# inner cross (extends past the ends to open the four end faces)
ix = cq.Workplane("YZ").circle(R - t).extrude(L / 2 + 1, both=True)
iy = cq.Workplane("XZ").circle(R - t).extrude(L / 2 + 1, both=True)
inner = ix.union(iy)

result = outer.cut(inner)
