import cadquery as cq

base = cq.Workplane("XY").circle(25).extrude(20)
cone = cq.Solid.makeCone(25, 0, 40, pnt=cq.Vector(0, 0, 20), dir=cq.Vector(0, 0, 1))
result = base.union(cq.Workplane("XY").add(cone))
