import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

result = base
for i in range(10):
    x = -27 + 6 * i
    fin = (cq.Workplane("XY")
           .workplane(offset=10)
           .center(x, 0)
           .rect(2, 60)
           .extrude(40))
    result = result.union(fin)
