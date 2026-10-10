import math
d = 50 / math.cos(math.radians(30))
result = (cq.Workplane("XY").polygon(6, d).extrude(20)
          .faces(">Z").edges().chamfer(2)
          .faces(">Z").workplane().hole(20))
