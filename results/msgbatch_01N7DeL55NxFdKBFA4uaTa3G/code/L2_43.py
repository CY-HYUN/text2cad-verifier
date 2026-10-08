import cadquery as cq

# Base 60x60x20 block
base = cq.Workplane("XY").rect(60, 60).extrude(20)

# Cut a centered 40x40 square through to form a frame
frame = base.faces(">Z").workplane().rect(40, 40).cutThruAll()

# Centered 40 mm diameter cylinder, 20 mm tall, filling the opening (tangent to the inner walls)
cyl = cq.Workplane("XY").circle(20).extrude(20)

result = frame.union(cyl)
