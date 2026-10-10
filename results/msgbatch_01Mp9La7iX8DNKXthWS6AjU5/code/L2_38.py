import cadquery as cq

# Outer cylinders (dia 50), centred at the origin
cyl_x = cq.Workplane("YZ").circle(25).extrude(60, both=True)   # length 120 along X
cyl_z = cq.Workplane("XY").circle(25).extrude(40, both=True)   # length 80 along Z
body = cyl_x.union(cyl_z)

# Bores (dia 40) from all four end faces to the centre, fully connected
bore_x = cq.Workplane("YZ").circle(20).extrude(60, both=True)
bore_z = cq.Workplane("XY").circle(20).extrude(40, both=True)
bores = bore_x.union(bore_z)

result = body.cut(bores)
