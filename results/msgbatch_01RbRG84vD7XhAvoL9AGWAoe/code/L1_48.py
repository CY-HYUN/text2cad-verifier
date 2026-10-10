import cadquery as cq

base = cq.Workplane("XY").box(40, 40, 20, centered=(True, True, False))
cyl = cq.Workplane("XY").workplane(offset=20).circle(10).extrude(20)
result = base.union(cyl)
