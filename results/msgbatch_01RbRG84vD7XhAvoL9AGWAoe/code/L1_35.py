import cadquery as cq

# Main cylinder: diameter 40, height 40, base at Z=0
cyl = cq.Workplane("XY").circle(20).extrude(40)

# Conical pit: 30 mm opening at the top face, tip 15 mm deep at Z=25
cone = cq.Solid.makeCone(15, 0, 15, pnt=cq.Vector(0, 0, 40), dir=cq.Vector(0, 0, -1))

result = cyl.cut(cq.Workplane("XY").add(cone))
