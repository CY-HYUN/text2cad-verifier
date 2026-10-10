import cadquery as cq

base = cq.Workplane("XY").box(100, 60, 20, centered=(True, True, False))
top = (cq.Workplane("XY").workplane(offset=20)
       .box(100, 30, 20, centered=(True, True, False)))
result = base.union(top)
