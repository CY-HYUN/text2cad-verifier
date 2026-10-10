import cadquery as cq
import math

# Cube frame
cube = cq.Workplane("XY").box(60, 60, 60)

# Cut three orthogonal through holes (dia 40) -> opens all six faces
cyl_len = 100
cx = cq.Workplane("YZ").circle(20).extrude(cyl_len / 2, both=True)
cy = cq.Workplane("XZ").circle(20).extrude(cyl_len / 2, both=True)
cz = cq.Workplane("XY").circle(20).extrude(cyl_len / 2, both=True)
frame = cube.cut(cx).cut(cy).cut(cz)

# Central sphere dia 30
sphere = cq.Workplane("XY").sphere(15)

result = frame.union(sphere)

# Connecting columns along 8 cube diagonals
r_col = 2.0
start = 10.0
end = 40.0
for sx in (-1, 1):
    for sy in (-1, 1):
        for sz in (-1, 1):
            d = cq.Vector(sx, sy, sz).normalized()
            p = d * start
            col = cq.Solid.makeCylinder(r_col, end - start, cq.Vector(p.x, p.y, p.z), d)
            result = result.union(cq.Workplane("XY").add(col))
