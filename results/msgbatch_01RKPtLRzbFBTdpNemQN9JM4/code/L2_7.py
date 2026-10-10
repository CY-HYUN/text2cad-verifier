import cadquery as cq

ring = cq.Workplane("XY").circle(30).extrude(15)
rod = cq.Workplane("XY").box(85, 20, 15, centered=(False, True, False)).translate((25, 0, 0))
body = ring.union(rod)
bore = cq.Workplane("XY").center(5, 0).circle(15).extrude(15)
hole = cq.Workplane("XY").center(100, 0).circle(5).extrude(15)
result = body.cut(bore).cut(hole)
