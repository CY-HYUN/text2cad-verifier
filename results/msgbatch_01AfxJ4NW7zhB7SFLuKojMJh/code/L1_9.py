import cadquery as cq

cyl = cq.Workplane("XY").circle(15).extrude(100)
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 115))
result = cyl.union(sphere)
