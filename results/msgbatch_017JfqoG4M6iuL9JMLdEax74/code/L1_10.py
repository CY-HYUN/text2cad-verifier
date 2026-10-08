import cadquery as cq

body = cq.Workplane("XY").box(100, 50, 30).translate((0, 0, 15))
slot = cq.Workplane("XY").box(102, 20, 15).translate((0, 0, 30 - 7.5))
result = body.cut(slot)
