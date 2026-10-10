import cadquery as cq

bar = cq.Workplane("XY").box(60, 20, 20)
stem = cq.Workplane("XY").box(20, 20, 60).translate((0, 0, -20))  # z from -50 to 10
body = bar.union(stem).clean()

shape = None
for r in (8, 7.5, 7, 6, 5):
    try:
        shape = body.edges().fillet(r)
        break
    except Exception:
        continue
if shape is None:
    shape = body

depth = 20
hole_d = 5

# hole at +X end
hx1 = cq.Workplane("YZ").workplane(offset=30 - depth).circle(hole_d / 2).extrude(depth + 1)
# hole at -X end
hx2 = cq.Workplane("YZ").workplane(offset=-31).circle(hole_d / 2).extrude(depth + 1)
# hole at bottom of stem (z=-50)
hz = cq.Workplane("XY").workplane(offset=-51).circle(hole_d / 2).extrude(depth + 1)

result = shape.cut(hx1).cut(hx2).cut(hz)
