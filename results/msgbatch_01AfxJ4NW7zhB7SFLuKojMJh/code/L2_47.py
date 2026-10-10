import cadquery as cq

L = 100.0
tube = cq.Workplane("XY").circle(15).extrude(L)
fl1 = cq.Workplane("XY").circle(25).extrude(5)
fl2 = cq.Workplane("XY").workplane(offset=L-5).circle(25).extrude(5)
baffle = cq.Workplane("XY").workplane(offset=L/2-2.5).circle(20).extrude(5)

body = tube.union(fl1).union(fl2).union(baffle)

bore1 = cq.Workplane("XY").circle(10).extrude(L/2-2.5)
bore2 = cq.Workplane("XY").workplane(offset=L/2+2.5).circle(10).extrude(L/2-2.5)

result = body.cut(bore1).cut(bore2)
