import cadquery as cq

L = 40.0
D = 10.0
R = D / 2.0

cube = cq.Workplane("XY").box(L, L, L)

hole_z = cq.Workplane("XY").circle(R).extrude(L * 2, both=True)
hole_x = cq.Workplane("YZ").circle(R).extrude(L * 2, both=True)
hole_y = cq.Workplane("XZ").circle(R).extrude(L * 2, both=True)

result = cube.cut(hole_z).cut(hole_x).cut(hole_y)
