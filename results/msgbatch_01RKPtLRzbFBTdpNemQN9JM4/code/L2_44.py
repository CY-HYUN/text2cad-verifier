import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))
result = base
for i in range(10):
    x = -27 + 6 * i
    fin = cq.Workplane("XY").box(2, 60, 40, centered=(True, True, False)).translate((x, 0, 10))
    result = result.union(fin)
