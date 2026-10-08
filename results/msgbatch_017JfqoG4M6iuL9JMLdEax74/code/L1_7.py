import cadquery as cq

a = cq.Workplane("XY").box(100, 20, 20)
b = cq.Workplane("XY").box(20, 100, 20)
result = a.union(b)
