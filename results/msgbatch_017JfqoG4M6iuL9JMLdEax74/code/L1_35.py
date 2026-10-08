import cadquery as cq

# Main body: 40 mm diameter x 40 mm tall, standing on Z=0
body = cq.Workplane("XY").circle(20).extrude(40)

# Conical pit: 30 mm diameter at the top face, tip 15 mm below it
cone = cq.Solid.makeCone(0.0, 15.0, 15.0,
                         pnt=cq.Vector(0, 0, 25),
                         dir=cq.Vector(0, 0, 1))

result = body.cut(cq.Workplane("XY").add(cone))
