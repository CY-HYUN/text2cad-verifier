import cadquery as cq

length = 100
lower = cq.Workplane("XY").box(length, 60, 20, centered=(False, True, False))
upper = (cq.Workplane("XY").workplane(offset=20)
         .box(length, 30, 20, centered=(False, True, False)))
result = lower.union(upper)
