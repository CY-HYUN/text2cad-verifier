import cadquery as cq

outer = cq.Workplane("XY").circle(40.0).extrude(20.0)
inner = cq.Workplane("XY").center(10.0, 0).circle(20.0).extrude(20.0)
result = outer.cut(inner)
