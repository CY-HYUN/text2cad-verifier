import cadquery as cq

sphere = cq.Workplane("XY").sphere(25)
hole = cq.Workplane("XY").circle(7).extrude(30, both=True)
result = sphere.cut(hole)
