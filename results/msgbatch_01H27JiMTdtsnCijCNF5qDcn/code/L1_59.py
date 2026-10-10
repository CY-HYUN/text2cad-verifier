import cadquery as cq
import math

cyl = cq.Workplane("XY").circle(30.0).extrude(80.0)

profile = (cq.Workplane("XZ")
           .polyline([(27, 35), (30, 35), (30, 45), (27, 45)]).close()
           .revolve(360, (0, 0, 0), (0, 1, 0)))

body = cyl.cut(profile)

class GrooveEdgeSelector(cq.Selector):
    def filter(self, objs):
        out = []
        for e in objs:
            if e.geomType() != "CIRCLE":
                continue
            c = e.Center()
            r = e.radius()
            if (abs(c.z - 35) < 1e-3 or abs(c.z - 45) < 1e-3) and (abs(r - 30) < 1e-3 or abs(r - 27) < 1e-3):
                out.append(e)
        return out

result = body.edges(GrooveEdgeSelector()).fillet(1.0)
