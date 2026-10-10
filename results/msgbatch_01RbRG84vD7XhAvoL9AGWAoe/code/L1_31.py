import cadquery as cq

sphere = cq.Workplane("XY").sphere(25)
hole = cq.Workplane("XY").box(20, 20, 60)
result = sphere.cut(hole)
