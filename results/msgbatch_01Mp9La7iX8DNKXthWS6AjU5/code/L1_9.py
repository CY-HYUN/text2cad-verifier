import cadquery as cq

cyl = cq.Workplane("XY").circle(15.0).extrude(100.0)
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 115.0))
result = cyl.union(sphere)
