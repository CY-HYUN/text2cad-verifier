import cadquery as cq
import math

def head(a, b, h):
    prof = (cq.Workplane("XZ")
            .moveTo(0, -h)
            .lineTo(a, -h)
            .lineTo(a, 0)
            .ellipseArc(a, b, 0, 90, startAtCurrent=True)
            .close())
    return prof.revolve(360, (0, 0, 0), (0, 1, 0))

# inner: semi-axes 100 x 50, straight section 25; outer offset by 8
inner = head(100, 50, 25)
outer = head(108, 58, 25)
shell = outer.cut(inner)

# flange on vertex: OD 40, ID 30, 30 mm above outer vertex (z=58 -> 88)
flange = cq.Workplane("XY").workplane(offset=50).circle(20).extrude(38)
body = shell.union(flange)

# bore through flange and shell top
bore = cq.Workplane("XY").workplane(offset=40).circle(15).extrude(60)
result = body.cut(bore)
