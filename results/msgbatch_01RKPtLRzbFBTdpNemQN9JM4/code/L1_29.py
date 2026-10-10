import cadquery as cq

bottom = cq.Workplane("XY").circle(30).extrude(10)
middle = cq.Workplane("XY").workplane(offset=10).circle(20).extrude(10)
top = cq.Workplane("XY").workplane(offset=20).circle(10).extrude(10)

result = bottom.union(middle).union(top)
