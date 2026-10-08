import cadquery as cq
import math

L = 60.0      # cube edge
D_hole = 40.0 # through-hole diameter on each face
D_sph = 30.0  # central sphere diameter
r_rod = 3.0   # connecting column radius

# Cube frame: cube minus three orthogonal through-cylinders
cube = cq.Workplane("XY").box(L, L, L)
cut_len = L * 2
cyl_z = cq.Workplane("XY").circle(D_hole / 2).extrude(cut_len / 2, both=True)
cyl_x = cq.Workplane("YZ").circle(D_hole / 2).extrude(cut_len / 2, both=True)
cyl_y = cq.Workplane("XZ").circle(D_hole / 2).extrude(cut_len / 2, both=True)
frame = cube.cut(cyl_z).cut(cyl_x).cut(cyl_y)

# Central sphere
sphere = cq.Workplane("XY").sphere(D_sph / 2)

# Connecting columns from center toward the 8 inner corners (along body diagonals)
rod_len = 45.0  # ends inside the solid corner region (diagonal to corner ~51.96)
model = frame.union(sphere)
for sx in (-1, 1):
    for sy in (-1, 1):
        for sz in (-1, 1):
            d = cq.Vector(sx, sy, sz).normalized()
            rod = cq.Solid.makeCylinder(r_rod, rod_len, cq.Vector(0, 0, 0), d)
            model = model.union(cq.Workplane("XY").add(rod))

result = model
