import cadquery as cq
import math

B = 40.0
H = 40.0

# Outer pyramid
outer = (cq.Workplane("XY").rect(B, B)
         .workplane(offset=H).rect(0.01, 0.01)
         .loft(combine=True))

# Inner cavity pyramid from base upward
b2 = 34.0
h2 = 34.0
cavity = (cq.Workplane("XY").rect(b2, b2)
          .workplane(offset=h2).rect(0.01, 0.01)
          .loft(combine=True))

body = outer.cut(cavity)

# Triangular through-holes on the side faces
tri = (cq.Workplane("XZ")
       .polyline([(-14, 3), (14, 3), (0, 31)]).close()
       .extrude(30, both=True))
tri2 = tri.rotate((0, 0, 0), (0, 0, 1), 90)

result = body.cut(tri).cut(tri2)
