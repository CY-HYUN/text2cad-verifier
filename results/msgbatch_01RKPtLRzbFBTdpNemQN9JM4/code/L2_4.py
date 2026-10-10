import cadquery as cq
import math

base = (cq.Workplane("XY").rect(100, 100).extrude(15)
        .edges("|Z").fillet(10))
sleeve = cq.Workplane("XY").workplane(offset=15).circle(30).extrude(40)
body = base.union(sleeve)
body = body.cut(cq.Workplane("XY").circle(20).extrude(55))
holes = (cq.Workplane("XY").rect(80, 80, forConstruction=True).vertices()
         .circle(5).extrude(15))
result = body.cut(holes)
