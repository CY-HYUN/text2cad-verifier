import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

n = 10
t = 2
spacing = (60 - t) / (n - 1)

result = base
for i in range(n):
    x0 = -30 + i * spacing + t / 2
    fin = (cq.Workplane("XY").workplane(offset=10)
           .center(x0, 0).rect(t, 60).extrude(40))
    result = result.union(fin)
