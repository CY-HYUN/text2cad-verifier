import cadquery as cq
import math

L = 60.0
hole_d = 40.0
sphere_d = 30.0
col_r = 2.0

# Cube frame
cube = cq.Workplane("XY").box(L, L, L)
cyl_z = cq.Workplane("XY").circle(hole_d / 2).extrude(L, both=True)
cyl_x = cq.Workplane("YZ").circle(hole_d / 2).extrude(L, both=True)
cyl_y = cq.Workplane("XZ").circle(hole_d / 2).extrude(L, both=True)
frame = cube.cut(cyl_z).cut(cyl_x).cut(cyl_y)

# Central sphere
sphere = cq.Workplane("XY").sphere(sphere_d / 2)

# Connecting columns along the 8 body diagonals toward inner corners
col_len = 20.0 * math.sqrt(3)  # reaches well into frame corner material
cols = None
for sx in (-1, 1):
    for sy in (-1, 1):
        for sz in (-1, 1):
            d = cq.Vector(sx, sy, sz).normalized()
            c = cq.Solid.makeCylinder(col_r, col_len, cq.Vector(0, 0, 0), d)
            cols = c if cols is None else cols.fuse(c)

result = frame.union(sphere).union(cq.Workplane("XY").add(cols))
