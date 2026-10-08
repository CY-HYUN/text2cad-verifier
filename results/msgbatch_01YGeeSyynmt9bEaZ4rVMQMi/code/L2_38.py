import cadquery as cq

# Outer cylinders, centred on the origin
cx = cq.Workplane("YZ").circle(25).extrude(60, both=True)  # along X, length 120
cz = cq.Workplane("XY").circle(25).extrude(40, both=True)  # along Z, length 80
outer = cx.union(cz)

# Inner bores, diameter 40, cut from all four end faces to the centre
hx = cq.Workplane("YZ").circle(20).extrude(60, both=True)
hz = cq.Workplane("XY").circle(20).extrude(40, both=True)

result = outer.cut(hx).cut(hz)
