import cadquery as cq

# Base block 60x60x20
base = cq.Workplane("XY").rect(60, 60).extrude(20)

# Cut a centered 40x40 square through the block to form a frame
frame = base.faces(">Z").workplane().rect(40, 40).cutThruAll()

# Cylinder of diameter 40, 20 mm tall, inside the frame opening
# (tangent to the inner walls at four points), merged with the frame
cyl = cq.Workplane("XY").circle(20).extrude(20)

result = frame.union(cyl)
