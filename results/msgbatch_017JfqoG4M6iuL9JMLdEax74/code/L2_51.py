import cadquery as cq
import math

L = 60.0
W = 20.0
R = 8.0
hole_d = 5.0
hole_depth = 12.0

# Cross bar along X, centered at origin
bar = cq.Workplane("XY").box(L, W, W)
# Stem along +Y, total length 60 starting at back face of bar
stem = cq.Workplane("XY").box(W, L, W).translate((0, L / 2 - W / 2, 0))

body = bar.union(stem).clean()

result = None
for r in (R, 7.5, 7.0, 6.0, 5.0):
    try:
        cand = body.edges().fillet(r)
        if cand.val().isValid():
            result = cand
            break
    except Exception:
        continue
if result is None:
    result = body

# Holes at three end faces
ends = [
    (cq.Vector(-L / 2, 0, 0), cq.Vector(1, 0, 0)),
    (cq.Vector(L / 2, 0, 0), cq.Vector(-1, 0, 0)),
    (cq.Vector(0, L - W / 2, 0), cq.Vector(0, -1, 0)),
]
for p, d in ends:
    start = p - d * 1.0
    cyl = cq.Solid.makeCylinder(hole_d / 2, hole_depth + 1.0, start, d)
    result = result.cut(cq.Workplane("XY").add(cyl))
