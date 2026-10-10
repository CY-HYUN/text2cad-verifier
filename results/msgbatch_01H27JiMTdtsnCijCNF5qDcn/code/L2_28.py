import cadquery as cq

outer = cq.Workplane("XY").box(60, 60, 60)
inner = cq.Workplane("XY").box(50, 50, 50)
shell = outer.cut(inner)

core = cq.Workplane("XY").box(20, 20, 20)

h = 51
rz = cq.Workplane("XY").circle(1).extrude(h / 2, both=True)
rx = cq.Workplane("YZ").circle(1).extrude(h / 2, both=True)
ry = cq.Workplane("XZ").circle(1).extrude(h / 2, both=True)

result = shell.union(core).union(rz).union(rx).union(ry)
