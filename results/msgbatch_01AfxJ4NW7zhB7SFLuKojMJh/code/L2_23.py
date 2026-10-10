import cadquery as cq
import math

t = 2.0

# Outer solid
sq = cq.Workplane("XY").rect(50, 50).extrude(20)
tr = (cq.Workplane("XY").workplane(offset=20).rect(50, 50)
      .workplane(offset=20).circle(15).loft(combine=True))
cy = cq.Workplane("XY").workplane(offset=40).circle(15).extrude(20)
outer = sq.union(tr).union(cy)

# Inner void (wall thickness 2 mm)
isq = cq.Workplane("XY").workplane(offset=-1).rect(46, 46).extrude(21)
itr = (cq.Workplane("XY").workplane(offset=20).rect(46, 46)
       .workplane(offset=20).circle(13).loft(combine=True))
icy = cq.Workplane("XY").workplane(offset=40).circle(13).extrude(21)
inner = isq.union(itr).union(icy)

result = outer.cut(inner)
