import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

cyl_z = cq.Workplane("XY").circle(20).extrude(40, both=True)
cyl_x = cq.Workplane("YZ").circle(20).extrude(40, both=True)
cyl_y = cq.Workplane("XZ").circle(20).extrude(40, both=True)

frame = cube.cut(cyl_z).cut(cyl_x).cut(cyl_y)

sphere = cq.Workplane("XY").sphere(15)

result = frame.union(sphere)
