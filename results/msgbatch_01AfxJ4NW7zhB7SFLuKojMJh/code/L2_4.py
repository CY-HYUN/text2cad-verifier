import cadquery as cq
import math

base = (cq.Workplane("XY").rect(100, 100).extrude(15)
        .edges("|Z").fillet(10))

sleeve = cq.Workplane("XY").workplane(offset=15).circle(30).extrude(40)
body = base.union(sleeve)

# central bore through everything
bore = cq.Workplane("XY").circle(20).extrude(55)
body = body.cut(bore)

# four mounting holes
holes = (cq.Workplane("XY")
         .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(5).extrude(15))
body = body.cut(holes)

result = body
