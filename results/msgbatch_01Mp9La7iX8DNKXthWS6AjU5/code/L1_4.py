import cadquery as cq

base = cq.Workplane("XY").circle(40.0).extrude(20.0)
upper = cq.Workplane("XY").workplane(offset=20.0).circle(20.0).extrude(30.0)
result = base.union(upper)
