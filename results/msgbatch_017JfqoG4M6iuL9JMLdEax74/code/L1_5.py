import cadquery as cq

# Square base plate: 60 x 60 mm, 10 mm thick, bottom face on Z = 0
base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

# Cylinder: 30 mm diameter, 50 mm tall, centred on the top face of the base
cyl = cq.Workplane("XY").workplane(offset=10).circle(15).extrude(50)

result = base.union(cyl)
