import cadquery as cq

L = 100.0
R_out = 30.0
R_in = 20.0

outer = cq.Workplane("YZ").circle(R_out).extrude(L).translate((-L / 2, 0, 0))
inner = cq.Workplane("YZ").circle(R_in).extrude(L).translate((-L / 2, 0, 0))
tube = outer.cut(inner)

half_box = cq.Workplane("XY").box(L + 2, 2 * R_out + 2, R_out + 1, centered=(True, True, False))
result = tube.intersect(half_box)
