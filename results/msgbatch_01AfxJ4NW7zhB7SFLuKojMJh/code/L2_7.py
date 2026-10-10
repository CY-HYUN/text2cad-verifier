import cadquery as cq

ring = cq.Workplane("XY").circle(30).extrude(15)
rod = cq.Workplane("XY").center(55, 0).rect(110, 20).extrude(15)
body = ring.union(rod)

bore = cq.Workplane("XY").center(5, 0).circle(15).extrude(15)
body = body.cut(bore)

hole = cq.Workplane("XY").center(100, 0).circle(5).extrude(15)
result = body.cut(hole)
