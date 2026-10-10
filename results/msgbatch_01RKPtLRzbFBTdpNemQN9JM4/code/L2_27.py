import cadquery as cq
import math

body = cq.Workplane("XY").circle(15).extrude(50)

d_circ = 15 / math.cos(math.radians(30))
hexcut = (cq.Workplane("XY").workplane(offset=25)
          .polygon(6, d_circ).extrude(25))
circcut = cq.Workplane("XY").circle(7.5).extrude(25)

result = body.cut(hexcut).cut(circcut)
