import cadquery as cq

bottom = cq.Workplane("XY").circle(30.0).extrude(10.0)
middle = cq.Workplane("XY").workplane(offset=10.0).circle(20.0).extrude(10.0)
top = cq.Workplane("XY").workplane(offset=20.0).circle(10.0).extrude(10.0)

result = bottom.union(middle).union(top)
