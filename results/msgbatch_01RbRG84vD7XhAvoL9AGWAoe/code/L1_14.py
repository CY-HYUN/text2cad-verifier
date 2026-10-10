import cadquery as cq

cyl = cq.Workplane("XY").circle(25).extrude(20)
cone = cq.Workplane("XY").add(
    cq.Solid.makeCone(25, 0, 40, pnt=cq.Vector(0, 0, 20), dir=cq.Vector(0, 0, 1))
)
result = cyl.union(cone)
