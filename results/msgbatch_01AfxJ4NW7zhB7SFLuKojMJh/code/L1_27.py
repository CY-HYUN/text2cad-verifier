import cadquery as cq

strip = cq.Workplane("XY").box(100, 20, 10, centered=False).translate((0, 0, 20))
block = cq.Workplane("XY").box(20, 20, 30, centered=False)
result = strip.union(block)
