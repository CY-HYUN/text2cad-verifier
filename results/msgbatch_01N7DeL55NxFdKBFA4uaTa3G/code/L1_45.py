import cadquery as cq

outer = cq.Workplane("XY").sphere(50.0)
inner = cq.Workplane("XY").sphere(40.0)

# Keep upper half (z >= 0) via intersection with a box
box_o = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))
outer_h = outer.intersect(box_o)
inner_h = inner.intersect(box_o)

result = outer_h.cut(inner_h)
