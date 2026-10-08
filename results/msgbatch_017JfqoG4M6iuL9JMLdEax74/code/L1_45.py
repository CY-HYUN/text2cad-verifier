import cadquery as cq

outer = cq.Workplane("XY").sphere(50)
inner = cq.Workplane("XY").sphere(40)
shell = outer.cut(inner)

# Keep only the upper half (z >= 0) so the cut plane faces downward
keep = cq.Workplane("XY").box(120, 120, 60, centered=(True, True, False))
result = shell.intersect(keep)
