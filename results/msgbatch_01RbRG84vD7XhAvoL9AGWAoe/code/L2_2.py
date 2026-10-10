import cadquery as cq
import math

R_sphere = 40.0
r_cyl = 15.0
offset = 25.0
h = 200.0

def build(off):
    sphere = cq.Workplane("XY").sphere(R_sphere)
    cyl = (
        cq.Workplane("XY")
        .workplane(offset=-h / 2)
        .center(off, 0)
        .circle(r_cyl)
        .extrude(h)
    )
    return sphere.cut(cyl)

result = None
for off in (offset, offset - 0.001, offset - 0.01):
    try:
        cand = build(off)
        if cand.val().isValid():
            result = cand
            break
    except Exception:
        pass

if result is None:
    result = build(offset - 0.01)
