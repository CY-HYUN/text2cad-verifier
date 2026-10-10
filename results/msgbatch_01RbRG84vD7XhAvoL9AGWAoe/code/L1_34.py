import cadquery as cq

length = 100.0
base_w, base_h = 60.0, 20.0
top_w, top_h = 30.0, 20.0

base = cq.Workplane("XY").box(length, base_w, base_h, centered=(True, True, False))
top = (cq.Workplane("XY").workplane(offset=base_h)
       .box(length, top_w, top_h, centered=(True, True, False)))
result = base.union(top)
