import cadquery as cq

L = 40.0
D = 10.0

# Cube centered on the origin
result = cq.Workplane("XY").box(L, L, L)

# Through-holes, each centred on the cube
cyl_z = cq.Workplane("XY").circle(D / 2).extrude(L * 2, both=True)
cyl_x = cq.Workplane("YZ").circle(D / 2).extrude(L * 2, both=True)
cyl_y = cq.Workplane("XZ").circle(D / 2).extrude(L * 2, both=True)

result = result.cut(cyl_z).cut(cyl_x).cut(cyl_y)
