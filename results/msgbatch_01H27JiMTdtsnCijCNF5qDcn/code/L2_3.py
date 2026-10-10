import cadquery as cq

sphere = cq.Workplane("XY").sphere(40)
keep = cq.Workplane("XY").box(100, 100, 40, centered=(True, True, False)).translate((0, 0, -40))
hemi = sphere.intersect(keep)

cut1 = cq.Workplane("XY").box(100, 10, 20, centered=(True, True, False)).translate((0, 0, -20))
cut2 = cq.Workplane("XY").box(10, 100, 20, centered=(True, True, False)).translate((0, 0, -20))

result = hemi.cut(cut1).cut(cut2)
