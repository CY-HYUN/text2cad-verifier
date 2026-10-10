import cadquery as cq

bar = cq.Workplane("XY").box(60, 20, 20)
stem = cq.Workplane("XY").box(20, 20, 60, centered=(True, True, False))
body = bar.union(stem).clean()

filleted = None
for r in [8, 7.5, 7, 6, 5, 4]:
    try:
        filleted = body.edges().fillet(r)
        if filleted.val().isValid():
            break
    except Exception:
        filleted = None
if filleted is None:
    filleted = body

depth = 25
hole_r = 2.5
h1 = cq.Workplane("YZ").workplane(offset=30 - depth).circle(hole_r).extrude(depth + 1)
h2 = cq.Workplane("YZ").workplane(offset=-30 - 1).circle(hole_r).extrude(depth + 1)
h3 = cq.Workplane("XY").workplane(offset=60 - depth).circle(hole_r).extrude(depth + 1)

result = filleted.cut(h1).cut(h2).cut(h3)
