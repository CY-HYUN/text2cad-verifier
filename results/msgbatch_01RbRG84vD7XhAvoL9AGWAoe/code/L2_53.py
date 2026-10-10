import cadquery as cq

L = 60.0
hole_d = 40.0
sphere_d = 30.0

# Base cube
cube = cq.Workplane("XY").box(L, L, L)

# Three through-cylinders (each covers two opposite faces)
cyl_len = L * 2
cz = cq.Workplane("XY").circle(hole_d / 2).extrude(cyl_len / 2, both=True)
cx = cq.Workplane("YZ").circle(hole_d / 2).extrude(cyl_len / 2, both=True)
cy = cq.Workplane("XZ").circle(hole_d / 2).extrude(cyl_len / 2, both=True)

frame = cube.cut(cz).cut(cx).cut(cy)

# Floating sphere in the central cavity
sphere = cq.Workplane("XY").sphere(sphere_d / 2)

result = frame.union(sphere)
