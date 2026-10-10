import cadquery as cq

outer = cq.Workplane("XY").sphere(50)
inner = cq.Workplane("XY").sphere(40)
shell = outer.cut(inner)
box = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))
result = shell.intersect(box)
