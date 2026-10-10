import cadquery as cq

large = cq.Workplane("XY").circle(25).extrude(50)
small = cq.Workplane("XY").center(40, 0).circle(15).extrude(50)

result = large.union(small)
