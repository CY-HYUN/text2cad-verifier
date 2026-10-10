import cadquery as cq

body = (cq.Workplane("XY").circle(30).extrude(15)
        .union(cq.Workplane("XY").center(40, 0).rect(80, 20).extrude(15)))

cut1 = cq.Workplane("XY").center(5, 0).circle(15).extrude(15)
cut2 = cq.Workplane("XY").center(70, 0).circle(5).extrude(15)

result = body.cut(cut1).cut(cut2)
