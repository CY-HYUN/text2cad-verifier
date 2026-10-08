import cadquery as cq

vertical = cq.Workplane("XY").box(10, 40, 60, centered=(False, False, False))
horizontal = cq.Workplane("XY").box(50, 40, 10, centered=(False, False, False))
result = vertical.union(horizontal)
