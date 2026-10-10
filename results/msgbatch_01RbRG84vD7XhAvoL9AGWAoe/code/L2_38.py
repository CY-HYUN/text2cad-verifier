import cadquery as cq

# Outer solids: horizontal pipe along X, vertical pipe along Z
horiz = cq.Workplane("YZ").circle(25).extrude(60, both=True)
vert = cq.Workplane("XY").circle(25).extrude(40, both=True)
body = horiz.union(vert)

# Bores: 40 mm through-holes along X and Z, crossing at the centre
bore_x = cq.Workplane("YZ").circle(20).extrude(61, both=True)
bore_z = cq.Workplane("XY").circle(20).extrude(41, both=True)

result = body.cut(bore_x).cut(bore_z)
