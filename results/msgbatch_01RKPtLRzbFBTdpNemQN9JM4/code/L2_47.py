import cadquery as cq

tube = cq.Workplane("XY").circle(15).extrude(100)
fl1 = cq.Workplane("XY").circle(25).extrude(5)
fl2 = cq.Workplane("XY").workplane(offset=95).circle(25).extrude(5)
body = tube.union(fl1).union(fl2)
bore = cq.Workplane("XY").circle(10).extrude(100)
body = body.cut(bore)
baffle = cq.Workplane("XY").workplane(offset=47.5).circle(20).extrude(5)
result = body.union(baffle)
