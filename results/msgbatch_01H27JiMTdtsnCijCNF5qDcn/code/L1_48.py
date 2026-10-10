import cadquery as cq

base = cq.Workplane("XY").rect(40, 40).extrude(20.0)
cyl = cq.Workplane("XY").workplane(offset=20.0).circle(10.0).extrude(20.0)
result = base.union(cyl)
