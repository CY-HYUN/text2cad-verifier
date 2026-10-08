import cadquery as cq

# Solid pipes: horizontal along X, vertical along Z
h = cq.Workplane("YZ").circle(25).extrude(60, both=True)
v = cq.Workplane("XY").circle(25).extrude(40, both=True)
body = h.union(v)

# Bores
hb = cq.Workplane("YZ").circle(20).extrude(61, both=True)
vb = cq.Workplane("XY").circle(20).extrude(41, both=True)

result = body.cut(hb).cut(vb)
