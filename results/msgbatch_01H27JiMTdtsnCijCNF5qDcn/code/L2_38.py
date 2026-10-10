import cadquery as cq

# Outer cylinders (diameter 50), centred at the origin
cyl_x = cq.Workplane("YZ").circle(25).extrude(60, both=True)   # length 120 along X
cyl_z = cq.Workplane("XY").circle(25).extrude(40, both=True)   # length 80 along Z
body = cyl_x.union(cyl_z)

# Bores (diameter 40) cut from each of the four end faces to the centre
bore_x = cq.Workplane("YZ").circle(20).extrude(60, both=True)
bore_z = cq.Workplane("XY").circle(20).extrude(40, both=True)

result = body.cut(bore_x).cut(bore_z)
