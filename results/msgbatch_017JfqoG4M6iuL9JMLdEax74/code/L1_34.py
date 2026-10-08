import cadquery as cq

L = 100.0
base = cq.Workplane("XY").box(L, 60, 20, centered=(True, True, False))
top = cq.Workplane("XY").workplane(offset=20).box(L, 30, 20, centered=(True, True, False))
result = base.union(top)
