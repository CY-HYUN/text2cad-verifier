import cadquery as cq
import math

def head(a, b, h):
    cyl = cq.Workplane("XY").circle(a).extrude(h)
    ell = (cq.Workplane("XZ").center(0, h).ellipse(a, b)
           .revolve(360, (0, 0, 0), (0, 1, 0)))
    box = cq.Workplane("XY").workplane(offset=h).rect(4*a, 4*a).extrude(b + 10)
    ell = ell.intersect(box)
    return cyl.union(ell)

outer = head(108, 58, 25)
inner = head(100, 50, 25)
shell = outer.cut(inner)

tube = (cq.Workplane("XY").workplane(offset=76).circle(20).extrude(37))
body = shell.union(tube)
bore = cq.Workplane("XY").workplane(offset=60).circle(15).extrude(60)
result = body.cut(bore)
