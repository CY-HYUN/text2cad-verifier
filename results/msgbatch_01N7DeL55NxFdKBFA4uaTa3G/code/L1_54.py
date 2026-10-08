import cadquery as cq

sphere = cq.Workplane("XY").sphere(25.0)
cyl = cq.Workplane("XY").workplane(offset=-30.0).circle(7.0).extrude(60.0)
result = sphere.cut(cyl)
