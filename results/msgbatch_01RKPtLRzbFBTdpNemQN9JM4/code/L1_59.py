import cadquery as cq
import math

cyl = cq.Workplane("XY").circle(30).extrude(80)
ring = (cq.Workplane("XY").workplane(offset=35)
        .circle(35).circle(27).extrude(10))
body = cyl.cut(ring)

class RSel(cq.Selector):
    def filter(self, objs):
        out = []
        for e in objs:
            try:
                r = e.radius()
            except Exception:
                continue
            z = e.Center().z
            if abs(r - 30) < 1e-3 and (abs(z - 35) < 1e-3 or abs(z - 45) < 1e-3):
                out.append(e)
        return out

result = body.edges(RSel()).fillet(1)
