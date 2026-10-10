import cadquery as cq

beam = cq.Workplane("XY").box(100, 20, 10, centered=False).translate((0, -10, 0))
base = cq.Workplane("XY").box(20, 20, 30, centered=False).translate((0, -10, -30))
result = beam.union(base)
