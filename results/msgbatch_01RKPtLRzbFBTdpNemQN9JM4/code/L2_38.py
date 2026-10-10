import cadquery as cq

hx = cq.Workplane("YZ").circle(25).extrude(60, both=True)
vz = cq.Workplane("XY").circle(25).extrude(40, both=True)
body = hx.union(vz)

holeX = cq.Workplane("YZ").circle(20).extrude(70, both=True)
holeZ = cq.Workplane("XY").circle(20).extrude(50, both=True)

result = body.cut(holeX).cut(holeZ)
