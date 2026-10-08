import cadquery as cq

big = cq.Workplane("XY").center(0, 0).circle(25.0).extrude(50.0)
small = cq.Workplane("XY").center(40.0, 0).circle(15.0).extrude(50.0)
result = big.union(small)
