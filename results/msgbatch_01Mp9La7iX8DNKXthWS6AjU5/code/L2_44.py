import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

n = 10
t = 2.0
pitch = (60 - t) / (n - 1)

result = base
for i in range(n):
    x = -30 + t / 2 + i * pitch
    fin = (cq.Workplane("XY").workplane(offset=10)
           .center(x, 0).rect(t, 60).extrude(40))
    result = result.union(fin)
