import cadquery as cq

sphere = cq.Workplane("XY").sphere(25)
hole = cq.Workplane("XY").circle(7).extrude(60).translate((0, 0, -30))
result = sphere.cut(hole)
