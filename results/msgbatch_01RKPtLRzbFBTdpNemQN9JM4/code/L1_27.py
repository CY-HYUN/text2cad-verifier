import cadquery as cq

strip = cq.Workplane("XY").box(100, 20, 10, centered=False).translate((0, 0, 30))
base = cq.Workplane("XY").box(20, 20, 30, centered=False)
result = base.union(strip)
