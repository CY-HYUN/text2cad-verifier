import cadquery as cq

L = 60.0
hole_d = 40.0
sphere_d = 30.0

# Base cube
frame = cq.Workplane("XY").box(L, L, L)

# Three through-cylinders (one per axis -> holes on all six faces)
r = hole_d / 2.0
cyl_z = cq.Workplane("XY").circle(r).extrude(L * 2).translate((0, 0, -L))
cyl_x = cq.Workplane("YZ").circle(r).extrude(L * 2).translate((-L, 0, 0))
cyl_y = cq.Workplane("XZ").circle(r).extrude(L * 2).translate((0, L, 0))

frame = frame.cut(cyl_z).cut(cyl_x).cut(cyl_y)

# Floating sphere in the central cavity
sphere = cq.Workplane("XY").sphere(sphere_d / 2.0)

result = frame.union(sphere)
