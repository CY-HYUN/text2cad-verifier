import cadquery as cq

base = cq.Workplane("XY").circle(40).extrude(20)
top = cq.Workplane("XY").workplane(offset=20).circle(20).extrude(30)
result = base.union(top)
