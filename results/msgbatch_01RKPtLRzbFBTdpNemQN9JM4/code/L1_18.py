import cadquery as cq

cyl = cq.Workplane("YZ").circle(15).extrude(60).translate((-30, 0, 0))
s1 = cq.Workplane("XY").sphere(15).translate((-30, 0, 0))
s2 = cq.Workplane("XY").sphere(15).translate((30, 0, 0))
result = cyl.union(s1).union(s2)
