import cadquery as cq

base = cq.Workplane("XY").rect(40, 40).extrude(20)
cyl = cq.Workplane("XY").workplane(offset=20).circle(10).extrude(20)
result = base.union(cyl)
