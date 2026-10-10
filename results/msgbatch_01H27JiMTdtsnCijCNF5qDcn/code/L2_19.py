import cadquery as cq

h = 50
t = 3  # brace thickness
outer = cq.Workplane("XY").circle(20).extrude(h)
bore = cq.Workplane("XY").circle(15).extrude(h)
cross = (cq.Workplane("XY").rect(40, t).extrude(h)
         .union(cq.Workplane("XY").rect(t, 40).extrude(h)))
cavity = bore.cut(cross)
result = outer.cut(cavity)
