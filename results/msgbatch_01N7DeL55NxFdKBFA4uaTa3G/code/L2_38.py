import cadquery as cq

# Outer cylinders, centred on the origin
cyl_x = cq.Workplane("YZ").circle(25).extrude(60, both=True)  # along X, total length 120
cyl_z = cq.Workplane("XY").circle(25).extrude(40, both=True)  # along Z, total length 80
outer = cyl_x.union(cyl_z)

# Inner bores (diameter 40) cut from each end face to the centre
bore_x = cq.Workplane("YZ").circle(20).extrude(60, both=True)
bore_z = cq.Workplane("XY").circle(20).extrude(40, both=True)

result = outer.cut(bore_x).cut(bore_z)
